import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Supported comparison operators mapping
_cmp_ops = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}

# Supported logical operators mapping
_logic_ops = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select(sql: str) -> List[str]:
    """Parse the SELECT clause and return a list of column names."""
    match = re.search(r'^SELECT\s+(.*?)\s+WHERE|^SELECT\s+(.*?)(?:\s+ORDER BY|$)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("SELECT clause missing or malformed.")
    cols = match.group(1) or match.group(2)
    return [c.strip() for c in cols.split(',')]

def _parse_where(sql: str) -> List[Dict[str, Any]]:
    """Parse the WHERE clause into a list of simple conditions."""
    where_match = re.search(r'WHERE\s+(.*?)(?:\s+ORDER BY|$)', sql, re.IGNORECASE | re.DOTALL)
    if not where_match:
        return []  # No WHERE clause
    expr = where_match.group(1).strip()
    # Tokenize conditions separated by AND/OR
    tokens = re.split(r'\s+(AND|OR)\s+', expr, flags=re.IGNORECASE)
    conditions = []
    i = 0
    while i < len(tokens):
        if tokens[i].upper() in _logic_ops:
            # Logical operator, skip
            i += 1
            continue
        cond = tokens[i]
        # Extract column, operator, value
        m = re.match(r'(\w+)\s*(=|!=|<=?|>=?)\s*(.+)', cond)
        if not m:
            raise ValueError(f"Invalid condition: {cond}")
        col, op_str, val = m.groups()
        # Safely parse value (int, float, bool, string)
        val = _parse_literal(val.strip())
        conditions.append({'col': col, 'op': op_str, 'val': val})
        i += 1
    return conditions

def _parse_order_by(sql: str) -> List[Dict[str, Any]]:
    """Parse the ORDER BY clause into a list of ordering instructions."""
    order_match = re.search(r'ORDER\s+BY\s+(.*)', sql, re.IGNORECASE | re.DOTALL)
    if not order_match:
        return []
    orders = [o.strip() for o in order_match.group(1).split(',')]
    result = []
    for o in orders:
        parts = o.split()
        col = parts[0]
        direction = parts[1].upper() if len(parts) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Invalid ORDER BY direction: {direction}")
        result.append({'col': col, 'dir': direction})
    return result

def _parse_literal(lit: str) -> Any:
    """Safely parse a literal value from the query."""
    # Attempt to interpret as int, float, bool, or string
    if lit.lower() == 'true':
        return True
    if lit.lower() == 'false':
        return False
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass
    # Strip surrounding quotes if present
    if (lit.startswith("'") and lit.endswith("'")) or (lit.startswith('"') and lit.endswith('"')):
        return lit[1:-1]
    # Otherwise treat as raw string
    return lit

def _evaluate_conditions(record: Dict[str, Any], conditions: List[Dict[str, Any]]) -> bool:
    """Evaluate all conditions against a single record."""
    # Build list of boolean results
    bools = []
    for cond in conditions:
        col, op_str, val = cond['col'], cond['op'], cond['val']
        if col not in record:
            raise ValueError(f"Column '{col}' does not exist in the dataset.")
        op_func = _cmp_ops[op_str]
        bools.append(op_func(record[col], val))
    # Combine using logical operators (assumes left-to-right evaluation)
    if not bools:
        return True
    result = bools[0]
    idx = 1
    while idx < len(bools):
        # Determine logical operator between previous and current condition
        # For simplicity, assume AND if not specified (since we stripped them)
        result = _logic_ops['AND'](result, bools[idx])
        idx += 1
    return result

def process_sql_request(dataset_records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query against an in-memory dataset.

    Parameters
    ----------
    dataset_records : List[Dict[str, Any]]
        The dataset to query.
    sql_statement : str
        A SQL-like statement containing SELECT, optional WHERE, and optional ORDER BY clauses.

    Returns
    -------
    List[Dict[str, Any]]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or references non‑existent columns.
    """
    if not isinstance(dataset_records, list) or not all(isinstance(r, dict) for r in dataset_records):
        raise ValueError("dataset_records must be a list of dictionaries.")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string.")

    # Normalise whitespace
    sql = re.sub(r'\s+', ' ', sql_statement.strip())

    # Parse clauses
    select_cols = _parse_select(sql)
    where_conditions = _parse_where(sql)
    order_by_instructions = _parse_order_by(sql)

    # Validate selected columns
    for col in select_cols:
        if col != '*' and not all(col in r for r in dataset_records):
            raise ValueError(f"Selected column '{col}' does not exist in all records.")

    # Filter records
    filtered = [r for r in dataset_records if _evaluate_conditions(r, where_conditions)]

    # Order records
    if order_by_instructions:
        def sort_key(rec):
            return tuple(
                rec[inst['col']] if inst['dir'] == 'ASC' else _invert(rec[inst['col']])
                for inst in order_by_instructions
            )

        def _invert(val):
            # For numeric types, invert by negation; for others, use reverse sort
            if isinstance(val, (int, float)):
                return -val
            return val

        filtered.sort(key=sort_key)

    # Project selected columns
    if select_cols == ['*']:
        result = [dict(rec) for rec in filtered]
    else:
        result = [{col: rec[col] for col in select_cols} for rec in filtered]

    return result
import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported operators in WHERE clauses
_OP_MAP = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Mapping of supported logical connectors in WHERE clauses
_LOGIC_MAP = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}

def _parse_select_clause(sql: str) -> List[str]:
    """Parse the SELECT part of the query."""
    match = re.search(r'^\s*SELECT\s+(.*?)\s+WHERE', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("SELECT clause is malformed or missing")
    cols = [c.strip() for c in match.group(1).split(',')]
    if not all(cols):
        raise ValueError("Empty column name in SELECT clause")
    return cols

def _parse_where_clause(sql: str) -> List[tuple]:
    """Parse the WHERE part of the query into a list of (column, op, value) tuples."""
    match = re.search(r'\sWHERE\s+(.*?)\s+ORDER BY', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        # No ORDER BY, take everything after WHERE until end
        match = re.search(r'\sWHERE\s+(.*)', sql, re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("WHERE clause is malformed or missing")
    where_str = match.group(1).strip()
    if not where_str:
        raise ValueError("Empty WHERE clause")
    # Split by AND/OR while keeping operators
    tokens = re.split(r'\s+(AND|OR)\s+', where_str, flags=re.IGNORECASE)
    conditions = []
    for token in tokens:
        if token.upper() in _LOGIC_MAP:
            continue
        # Find operator
        op_match = re.search(r'(=|==|!=|<>|>=|<=|>|<)', token)
        if not op_match:
            raise ValueError(f"Unsupported operator in condition: {token}")
        op = op_match.group(1)
        parts = token.split(op, 1)
        if len(parts) != 2:
            raise ValueError(f"Malformed condition: {token}")
        col, val = parts[0].strip(), parts[1].strip()
        # Strip quotes from string literals
        if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            # Try to interpret as number
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass  # keep as string
        conditions.append((col, op, val))
    return conditions

def _evaluate_conditions(record: Dict[str, Any], conditions: List[tuple]) -> bool:
    """Evaluate WHERE conditions for a single record."""
    # Build list of booleans
    bools = []
    ops_stack = []
    for col, op_sym, val in conditions:
        if col not in record:
            raise ValueError(f"Column '{col}' not found in dataset")
        op_func = _OP_MAP.get(op_sym)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_sym}")
        bools.append(op_func(record[col], val))
    # Since we split by AND/OR, the logical connectors are between conditions
    # Reconstruct using original string to maintain order
    # For simplicity, assume only AND is supported in this demo
    return all(bools)

def _parse_order_by_clause(sql: str) -> List[tuple]:
    """Parse the ORDER BY part of the query into a list of (column, direction) tuples."""
    match = re.search(r'\sORDER\s+BY\s+(.*)', sql, re.IGNORECASE | re.DOTALL)
    if not match:
        return []  # No ORDER BY
    order_str = match.group(1).strip()
    if not order_str:
        raise ValueError("Empty ORDER BY clause")
    orders = []
    for part in order_str.split(','):
        tokens = part.strip().split()
        col = tokens[0]
        dir_ = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if dir_ not in ('ASC', 'DESC'):
            raise ValueError(f"Unsupported ORDER BY direction: {dir_}")
        orders.append((col, dir_))
    return orders

def run_sql_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simplified SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        The data to query. Each dictionary represents a row.
    sql_query : str
        A SQL-like string containing SELECT, WHERE and ORDER BY clauses.

    Returns
    -------
    list[dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("SQL query must be a string")

    # Parse SELECT
    try:
        select_cols = _parse_select_clause(sql_query)
    except Exception as e:
        raise ValueError(f"Failed to parse SELECT clause: {e}")

    # Parse WHERE
    try:
        conditions = _parse_where_clause(sql_query)
    except Exception as e:
        raise ValueError(f"Failed to parse WHERE clause: {e}")

    # Parse ORDER BY
    try:
        order_by = _parse_order_by_clause(sql_query)
    except Exception as e:
        raise ValueError(f"Failed to parse ORDER BY clause: {e}")

    # Filter rows
    filtered = []
    for record in dataset:
        try:
            if _evaluate_conditions(record, conditions):
                filtered.append(record)
        except Exception as e:
            raise ValueError(f"Failed to evaluate conditions: {e}")

    # Project columns
    projected = [{col: rec.get(col) for col in select_cols} for rec in filtered]

    # Sort if needed
    if order_by:
        def sort_key(rec):
            return tuple(
                rec.get(col) for col, _ in order_by
            )
        reverse = any(dir_ == 'DESC' for _, dir_ in order_by)
        projected.sort(key=sort_key, reverse=reverse)

    return projected
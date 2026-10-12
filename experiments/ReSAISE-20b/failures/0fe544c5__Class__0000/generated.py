import re
import operator
from functools import reduce

# Mapping of supported operators to Python functions
_OPS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Supported logical operators
_LOGICAL_OPS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select_clause(sql):
    """
    Extract column names from SELECT clause.
    Supports '*' for all columns.
    """
    match = re.search(r'SELECT\s+(.*?)\s+FROM', sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("Missing SELECT clause")
    cols = [c.strip() for c in match.group(1).split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return ['*']
    if any(not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) for c in cols):
        raise ValueError("Invalid column names")
    return cols

def _parse_where_clause(sql):
    """
    Return a function that evaluates the WHERE condition for a record.
    Supports simple comparisons and AND/OR combinations without parentheses.
    """
    match = re.search(r'WHERE\s+(.*?)(?:\s+ORDER\s+BY|\s*$)', sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return lambda rec: True  # no WHERE clause
    condition = match.group(1).strip()
    if not condition:
        return lambda rec: True

    # Tokenize the condition
    tokens = re.split(r'\s+', condition)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    def eval_token(tok, rec):
        # Check if token is a logical operator
        up = tok.upper()
        if up in _LOGICAL_OPS:
            return up  # placeholder
        # Check for comparison expression
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(=|!=|<>|>=|<=|>|<)\s*([A-Za-z_][A-Za-z0-9_]*)$', tok)
        if m:
            field, op_sym, value = m.groups()
            if field not in rec:
                raise ValueError(f"Field {field} does not exist")
            # Treat value as string literal if it is quoted, else numeric
            val = value.strip()
            if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                val = val[1:-1]
            else:
                try:
                    if '.' in val:
                        val = float(val)
                    else:
                        val = int(val)
                except ValueError:
                    pass  # keep as string
            return _OPS[op_sym](rec[field], val)
        raise ValueError(f"Unsupported token in WHERE clause: {tok}")

    # Build a simple evaluator that handles AND/OR left-to-right
    def evaluator(rec):
        result = None
        current_op = None
        for tok in tokens:
            val = eval_token(tok, rec)
            if isinstance(val, str) and val in _LOGICAL_OPS:
                current_op = val
            else:
                if result is None:
                    result = val
                elif current_op:
                    result = _LOGICAL_OPS[current_op](result, val)
                    current_op = None
                else:
                    raise ValueError("Missing logical operator between conditions")
        return bool(result)

    return evaluator

def _parse_order_by_clause(sql):
    """
    Parse ORDER BY clause and return a list of (field, direction) tuples.
    Direction is True for ASC, False for DESC.
    """
    match = re.search(r'ORDER\s+BY\s+(.*?)(?:\s*$)', sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    clause = match.group(1).strip()
    if not clause:
        return []

    parts = [p.strip() for p in clause.split(',')]
    orderings = []
    for part in parts:
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(ASC|DESC)?$', part, flags=re.IGNORECASE)
        if not m:
            raise ValueError(f"Invalid ORDER BY clause: {part}")
        field, direction = m.groups()
        orderings.append((field, (direction or 'ASC').upper() == 'ASC'))
    return orderings

def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    sql_command : str
        Query string.

    Returns
    -------
    list[dict]
        Resulting records after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or evaluation fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    if not isinstance(sql_command, str):
        raise ValueError("sql_command must be a string")

    # Normalize whitespace
    sql = ' '.join(sql_command.strip().split())

    try:
        select_cols = _parse_select_clause(sql)
        where_func = _parse_where_clause(sql)
        order_by = _parse_order_by_clause(sql)

        # Filter records
        filtered = [rec for rec in records if where_func(rec)]

        # Order records
        if order_by:
            def sort_key(rec):
                return tuple(
                    rec.get(field, None) if asc else _reverse_value(rec.get(field, None))
                    for field, asc in order_by
                )
            filtered.sort(key=sort_key)

        # Project columns
        if select_cols == ['*']:
            result = filtered
        else:
            result = []
            for rec in filtered:
                proj = {}
                for col in select_cols:
                    if col not in rec:
                        raise ValueError(f"Field {col} does not exist in record")
                    proj[col] = rec[col]
                result.append(proj)

        return result
    except Exception as exc:
        raise ValueError(f"Query execution failed: {exc}") from exc

def _reverse_value(val):
    """
    Helper to reverse ordering for descending sort.
    Works for numbers and strings. For None, returns a high sentinel.
    """
    if val is None:
        return (1, None)  # place None at the end
    if isinstance(val, (int, float)):
        return (-val, val)
    if isinstance(val, str):
        return (''.join(chr(255 - ord(c)) for c in val), val)
    return (1, None)
import re
import operator
from functools import reduce

# Supported operators for WHERE clause comparisons
_OP_MAP = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

def _parse_select(query):
    """
    Extract the SELECT clause and return a list of columns.
    Supports '*' for all columns.
    """
    match = re.search(r'\bSELECT\s+(.*?)\s+WHERE\b', query, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("Missing SELECT clause or malformed query.")
    cols = [c.strip() for c in match.group(1).split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return ['*']
    if any(not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) for c in cols):
        raise ValueError("Invalid column names in SELECT clause.")
    return cols

def _parse_where(query):
    """
    Extract the WHERE clause expression.
    Supports simple binary comparisons combined with AND/OR (no parentheses).
    """
    match = re.search(r'\bWHERE\s+(.*?)\s*(ORDER BY|$)', query, re.IGNORECASE | re.DOTALL)
    if not match:
        return None  # No WHERE clause
    expr = match.group(1).strip()
    if not expr:
        return None

    # Tokenize into conditions and logical operators
    tokens = re.split(r'\s+(AND|OR)\s+', expr, flags=re.IGNORECASE)
    conditions = []
    logical_ops = []

    for i, token in enumerate(tokens):
        if i % 2 == 0:  # condition
            cond_match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=|>=|<=|>|<|=)\s*(.+)$', token)
            if not cond_match:
                raise ValueError(f"Invalid condition: {token}")
            field, op_str, value = cond_match.groups()
            # Normalize string literals (single or double quotes)
            if re.match(r"^(['\"])(.*)\1$", value):
                value = re.match(r"^(['\"])(.*)\1$", value).group(2)
            else:
                # Try to interpret as number
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass  # keep as string
            if op_str not in _OP_MAP:
                raise ValueError(f"Unsupported operator: {op_str}")
            conditions.append((field, _OP_MAP[op_str], value))
        else:  # logical operator
            logical_ops.append(token.upper())
    return conditions, logical_ops

def _parse_order_by(query):
    """
    Extract ORDER BY clause and return a list of (column, direction) tuples.
    Direction is 1 for ASC, -1 for DESC. Default is ASC.
    """
    match = re.search(r'\bORDER BY\s+(.*)$', query, re.IGNORECASE | re.DOTALL)
    if not match:
        return []  # No ORDER BY
    order_clause = match.group(1).strip()
    orders = []
    for part in order_clause.split(','):
        part = part.strip()
        if not part:
            continue
        tokens = part.split()
        col = tokens[0]
        if len(tokens) > 1:
            dir_token = tokens[1].upper()
            if dir_token not in ('ASC', 'DESC'):
                raise ValueError(f"Invalid ORDER BY direction: {dir_token}")
            dir_val = 1 if dir_token == 'ASC' else -1
        else:
            dir_val = 1
        orders.append((col, dir_val))
    return orders

def _apply_where(row, conditions, logical_ops):
    """
    Evaluate the WHERE clause for a single row.
    """
    if not conditions:
        return True
    # Evaluate first condition
    field, op_func, value = conditions[0]
    if field not in row:
        return False
    result = op_func(row[field], value)
    # Combine with subsequent conditions using logical operators
    for i, (field, op_func, value) in enumerate(conditions[1:]):
        if field not in row:
            next_res = False
        else:
            next_res = op_func(row[field], value)
        if logical_ops[i] == 'AND':
            result = result and next_res
        elif logical_ops[i] == 'OR':
            result = result or next_res
    return result

def execute_custom_query(data, query):
    """
    Execute a simple SQL-like SELECT query on a list of dictionaries.

    Parameters
    ----------
    data : list[dict]
        The dataset to query.
    query : str
        SQL-like query string. Supports SELECT, WHERE, ORDER BY.

    Returns
    -------
    list[dict]
        Query result set.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries.")
    if not isinstance(query, str):
        raise ValueError("Query must be a string.")

    # Normalize whitespace
    query = re.sub(r'\s+', ' ', query.strip())

    try:
        select_cols = _parse_select(query)
        where_clause, logical_ops = _parse_where(query) or (None, None)
        order_by = _parse_order_by(query)
    except Exception as exc:
        raise ValueError(f"Failed to parse query: {exc}") from exc

    # Filter rows
    if where_clause:
        filtered = [row for row in data if _apply_where(row, where_clause, logical_ops)]
    else:
        filtered = list(data)

    # Order rows
    if order_by:
        def sort_key(row):
            return tuple(
                row.get(col, None) if dir_val == 1 else _reverse_value(row.get(col, None))
                for col, dir_val in order_by
            )
        # Helper to invert comparison for DESC
        def _reverse_value(val):
            if isinstance(val, (int, float)):
                return -val
            # For strings, reverse by using a tuple that sorts descending
            return val[::-1] if isinstance(val, str) else val

        filtered.sort(key=sort_key)

    # Project columns
    if select_cols == ['*']:
        result = [dict(row) for row in filtered]
    else:
        result = []
        for row in filtered:
            projected = {}
            for col in select_cols:
                if col not in row:
                    raise ValueError(f"Column '{col}' does not exist in data.")
                projected[col] = row[col]
            result.append(projected)

    return result
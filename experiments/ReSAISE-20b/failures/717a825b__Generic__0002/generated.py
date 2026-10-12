import re
import operator
from functools import reduce

# Mapping of string operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regex patterns for parsing the query
SELECT_PATTERN = re.compile(
    r'^SELECT\s+(?P<cols>[\w\s,]+)'
    r'(?:\s+WHERE\s+(?P<where>.+?))?'
    r'(?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?\s*$', re.IGNORECASE)

# Regex pattern for parsing a single condition (only one condition supported)
COND_PATTERN = re.compile(
    r'^(?P<field>\w+)\s*(?P<op>=|!=|>|<|>=|<=)\s*(?P<value>.+)$')

def _parse_value(val: str):
    """Try to convert the value string into int, float or strip quotes."""
    val = val.strip()
    # Remove surrounding quotes if present
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    # Try int
    try:
        return int(val)
    except ValueError:
        pass
    # Try float
    try:
        return float(val)
    except ValueError:
        pass
    # Return as string if surrounded by quotes
    return val

def _build_where_func(field: str, op_str: str, value):
    """Return a function that evaluates the condition on a row."""
    op_func = OPERATORS[op_str]
    def func(row):
        if field not in row:
            return False
        try:
            return op_func(row[field], value)
        except Exception:
            return False
    return func

def execute_custom_query(data, query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT col1, col2 [WHERE field op value] [ORDER BY field ASC|DESC]

    Args:
        data (list[dict]): The dataset.
        query (str): The SQL-like query string.

    Returns:
        list[dict]: The resulting rows with selected columns.

    Raises:
        ValueError: If the query is malformed or cannot be executed.
    """
    if not isinstance(data, list):
        raise ValueError("Data must be a list of dictionaries.")
    if not isinstance(query, str):
        raise ValueError("Query must be a string.")

    match = SELECT_PATTERN.match(query)
    if not match:
        raise ValueError("Query syntax is invalid.")

    # Parse selected columns
    cols_str = match.group('cols')
    selected_cols = [c.strip() for c in cols_str.split(',')]
    if not all(selected_cols):
        raise ValueError("SELECT clause must specify at least one column.")

    # Parse WHERE clause
    where_func = None
    if match.group('where'):
        cond_str = match.group('where')
        cond_match = COND_PATTERN.match(cond_str)
        if not cond_match:
            raise ValueError("WHERE clause syntax is invalid.")
        field = cond_match.group('field')
        op_str = cond_match.group('op')
        value_raw = cond_match.group('value')
        value = _parse_value(value_raw)
        where_func = _build_where_func(field, op_str, value)

    # Parse ORDER BY clause
    order_field = match.group('order')
    order_dir = match.group('dir') or 'ASC'
    reverse = order_dir.upper() == 'DESC'

    # Filter rows
    filtered_rows = []
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("Each item in data must be a dictionary.")
        if where_func is None or where_func(row):
            filtered_rows.append(row)

    # Sort rows if ORDER BY specified
    if order_field:
        try:
            filtered_rows.sort(key=lambda r: r.get(order_field, None), reverse=reverse)
        except TypeError:
            raise ValueError("Cannot sort by the specified field.")

    # Project selected columns
    result = []
    for row in filtered_rows:
        projected = {col: row.get(col, None) for col in selected_cols}
        result.append(projected)

    return result
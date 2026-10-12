import re
import operator
from functools import reduce

# Mapping of string operators to actual Python functions
OPS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def _parse_value(val_str):
    """Parse a value string into int, float or stripped string."""
    val_str = val_str.strip()
    if (val_str.startswith("'") and val_str.endswith("'")) or \
       (val_str.startswith('"') and val_str.endswith('"')):
        return val_str[1:-1]
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        # fallback to string without quotes
        return val_str

def _evaluate_condition(row, field, op_func, value):
    """Return True if the condition holds for the given row."""
    # Missing keys evaluate as False
    if field not in row:
        return False
    try:
        return op_func(row[field], value)
    except Exception:
        # type mismatch or other error
        return False

def execute_custom_query(data, query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <field1>, <field2>, ... 
            [WHERE <field> <operator> <value>] 
            [ORDER BY <field> [ASC|DESC]]

    Only a single WHERE condition is allowed. Supported operators are:
        =, !=, >, <, >=, <=
    ORDER BY can be ascending (ASC) or descending (DESC). ASC is default.

    Parameters
    ----------
    data : list[dict]
        Dataset to query.
    query : str
        Query string.

    Returns
    -------
    list[dict]
        Resulting rows with selected fields.

    Raises
    ------
    ValueError
        If the query syntax is invalid or cannot be executed.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries.")

    # Basic regex patterns
    select_pat = r"SELECT\s+(?P<select>[\w,\s]+)"
    where_pat  = r"(?:\s+WHERE\s+(?P<where>.+?))?"
    order_pat  = r"(?:\s+ORDER\s+BY\s+(?P<order>[\w]+)(?:\s+(?P<dir>ASC|DESC))?)?"
    full_pat   = f"^{select_pat}{where_pat}{order_pat}\\s*$"

    match = re.match(full_pat, query.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Invalid query syntax.")

    # Parse SELECT fields
    select_fields = [f.strip() for f in match.group('select').split(',')]
    if not select_fields or any(not f for f in select_fields):
        raise ValueError("SELECT clause must specify at least one field.")

    # Parse WHERE condition if present
    where_clause = match.group('where')
    filter_func = None
    if where_clause:
        # Simple pattern: field operator value
        cond_pat = r"(?P<field>\w+)\s*(?P<op>!=|>=|<=|=|>|<)\s*(?P<value>.+)"
        cond_match = re.match(cond_pat, where_clause.strip())
        if not cond_match:
            raise ValueError("Invalid WHERE clause.")
        field = cond_match.group('field')
        op_str = cond_match.group('op')
        value_raw = cond_match.group('value')
        if op_str not in OPS:
            raise ValueError(f"Unsupported operator '{op_str}'.")
        op_func = OPS[op_str]
        value = _parse_value(value_raw)

        def filter_func(row):
            return _evaluate_condition(row, field, op_func, value)

    # Parse ORDER BY if present
    order_field = match.group('order')
    order_dir   = match.group('dir')
    reverse = False
    if order_field:
        reverse = (order_dir or 'ASC').upper() == 'DESC'
        def sort_key(row):
            return row.get(order_field, None)
    else:
        sort_key = None

    # Filter data
    result_rows = (row for row in data if filter_func(row) if filter_func else True)

    # Convert to list for sorting
    result_list = list(result_rows)

    # Sort if needed
    if sort_key:
        try:
            result_list.sort(key=sort_key, reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot sort by field '{order_field}': {e}")

    # Project selected fields
    final_result = []
    for row in result_list:
        projected = {}
        for f in select_fields:
            if f not in row:
                raise ValueError(f"Field '{f}' does not exist in data.")
            projected[f] = row[f]
        final_result.append(projected)

    return final_result
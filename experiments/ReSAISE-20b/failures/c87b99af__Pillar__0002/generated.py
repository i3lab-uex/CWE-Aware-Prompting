import re
import operator
from functools import reduce

# Mapping of supported comparison operators to functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(r'^SELECT\s+(?P<cols>[\*\w,\s]+)\s+WHERE\s+(?P<where>.+?)\s*(ORDER BY\s+(?P<order>\w+))?\s*$', re.IGNORECASE)
WHERE_COND_RE = re.compile(r'(?P<field>\w+)\s*(?P<op>=|!=|<>|<=|>=|<|>)\s*(?P<value>.+?)', re.IGNORECASE)
AND_OR_RE = re.compile(r'\s+(AND|OR)\s+', re.IGNORECASE)

def _parse_value(val: str):
    """Convert a string literal to its Python type."""
    val = val.strip()
    if val.startswith(("'", '"')) and val.endswith(("'", '"')):
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
    # If it looks like a boolean
    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False
    # Otherwise keep as string
    return val

def _build_where_func(where_clause: str):
    """Return a function that evaluates the WHERE clause for a record."""
    # Split by AND/OR
    tokens = [t.strip() for t in AND_OR_RE.split(where_clause)]
    ops = [m.group(1).upper() for m in AND_OR_RE.finditer(where_clause)]

    # Build individual condition functions
    cond_funcs = []
    for token in tokens:
        m = WHERE_COND_RE.fullmatch(token)
        if not m:
            raise ValueError(f"Invalid condition in WHERE clause: '{token}'")
        field = m.group('field')
        op_str = m.group('op')
        value_raw = m.group('value')
        op_func = OPERATORS.get(op_str)
        if not op_func:
            raise ValueError(f"Unsupported operator '{op_str}' in WHERE clause")
        value = _parse_value(value_raw)

        def cond(record, f=field, op=op_func, v=value):
            if f not in record:
                return False
            try:
                return op(record[f], v)
            except Exception:
                return False

        cond_funcs.append(cond)

    # Combine using AND/OR
    def where_func(record):
        result = cond_funcs[0](record)
        for op, func in zip(ops, cond_funcs[1:]):
            if op == 'AND':
                result = result and func(record)
            elif op == 'OR':
                result = result or func(record)
            else:
                raise ValueError(f"Unsupported logical operator '{op}'")
        return result

    return where_func


def execute_user_query(records, user_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    user_query : str
        SQL-like query string.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query format is invalid or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    for r in records:
        if not isinstance(r, dict):
            raise ValueError("All items in records must be dictionaries")

    match = SELECT_RE.fullmatch(user_query.strip())
    if not match:
        raise ValueError("Query must be of the form: SELECT <cols> WHERE <condition> [ORDER BY <col>]")

    cols_raw = match.group('cols')
    where_clause = match.group('where')
    order_col = match.group('order')

    # Determine columns to select
    if cols_raw.strip() == '*':
        selected_cols = None  # all columns
    else:
        selected_cols = [c.strip() for c in cols_raw.split(',')]
        if not all(selected_cols):
            raise ValueError("Column names cannot be empty")

    # Build WHERE function
    where_func = _build_where_func(where_clause)

    # Filter records
    try:
        filtered = [rec for rec in records if where_func(rec)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Order by if specified
    if order_col:
        try:
            filtered.sort(key=lambda rec: rec.get(order_col))
        except Exception as e:
            raise ValueError(f"Error ordering by '{order_col}': {e}")

    # Project columns
    result = []
    for rec in filtered:
        if selected_cols is None:
            projected = dict(rec)  # copy all
        else:
            projected = {c: rec.get(c) for c in selected_cols}
        result.append(projected)

    return result
import re
import operator
from functools import reduce

# mapping of supported comparison operators
_OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# mapping of supported logical operators
_LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# pattern for parsing the SQL-like query
_QUERY_RE = re.compile(
    r'''
    ^\s*SELECT\s+(?P<columns>[\w*,\s]+?)          # columns list
    (?:\s+WHERE\s+(?P<where>.+?))?                # optional WHERE clause
    (?:\s+ORDER\s+BY\s+(?P<order_by>[\w]+)        # optional ORDER BY
    (?:\s+(?P<order_dir>ASC|DESC))?)?\s*$
    ''',
    re.IGNORECASE | re.VERBOSE
)

# pattern for parsing individual conditions (simple binary ops)
_COND_RE = re.compile(
    r'''
    (?P<field>\w+)\s*
    (?P<op>=|!=|<>|<=?|>=?)\s*
    (?P<value>[^ ]+)
    ''',
    re.VERBOSE
)

def _parse_value(val: str):
    """Convert a literal value to int/float or strip quotes."""
    # Try integer
    if re.fullmatch(r'-?\d+', val):
        return int(val)
    # Try float
    if re.fullmatch(r'-?\d+\.\d*', val):
        return float(val)
    # Strip quotes if present
    if (val.startswith("'") and val.endswith("'")) or \
       (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Return as is (string)
    return val

def _build_condition(cond_str: str):
    """Build a function that evaluates the condition on a record."""
    # Split logical operators
    tokens = re.split(r'\s+(AND|OR)\s+', cond_str, flags=re.IGNORECASE)
    funcs = []
    logical_ops = []

    for i, token in enumerate(tokens):
        if i % 2 == 0:  # condition
            m = _COND_RE.fullmatch(token.strip())
            if not m:
                raise ValueError(f"Invalid condition: '{token}'")
            field = m.group('field')
            op_str = m.group('op')
            value_raw = m.group('value')
            comp_op = _OPERATORS.get(op_str)
            if not comp_op:
                raise ValueError(f"Unsupported operator: '{op_str}'")
            value = _parse_value(value_raw)

            def make_cond(field, comp_op, value):
                return lambda rec: comp_op(rec.get(field), value)

            funcs.append(make_cond(field, comp_op, value))
        else:  # logical operator
            logical_ops.append(token.upper())

    def eval_cond(rec):
        result = funcs[0](rec)
        for op, func in zip(logical_ops, funcs[1:]):
            result = _LOGICAL_OPERATORS[op](result, func(rec))
        return result

    return eval_cond

def run_user_query(dataset: list[dict], sql_query: str) -> list[dict]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        The dataset to query.
    sql_query : str
        SQL-like query string supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query syntax is invalid or execution fails.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    m = _QUERY_RE.fullmatch(sql_query)
    if not m:
        raise ValueError("Invalid query format")

    # Parse SELECT columns
    cols_raw = m.group('columns')
    select_cols = [c.strip() for c in cols_raw.split(',')]
    if not all(select_cols):
        raise ValueError("Empty column name in SELECT clause")
    # Validate columns exist
    if dataset:
        for col in select_cols:
            if col not in dataset[0]:
                raise ValueError(f"Column '{col}' does not exist in dataset")

    # Build WHERE filter
    where_str = m.group('where')
    if where_str:
        try:
            cond_func = _build_condition(where_str)
        except Exception as e:
            raise ValueError(f"Invalid WHERE clause: {e}") from None
        filtered = [rec for rec in dataset if cond_func(rec)]
    else:
        filtered = list(dataset)

    # ORDER BY
    order_by_col = m.group('order_by')
    if order_by_col:
        if order_by_col not in dataset[0]:
            raise ValueError(f"Order column '{order_by_col}' does not exist")
        dir_str = m.group('order_dir')
        reverse = (dir_str or '').upper() == 'DESC'
        try:
            filtered.sort(key=lambda rec: rec.get(order_by_col), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Failed to sort by '{order_by_col}': {e}") from None

    # Project selected columns
    result = [{col: rec.get(col) for col in select_cols} for rec in filtered]
    return result
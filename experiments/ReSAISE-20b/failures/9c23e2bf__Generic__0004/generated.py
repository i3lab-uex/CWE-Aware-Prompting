import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Mapping of supported comparison operators to functions
_OPERATOR_MAP = {
    '=': eq,
    '==': eq,
    '!=': ne,
    '<>': ne,
    '>': gt,
    '>=': ge,
    '<': lt,
    '<=': le,
}

def _parse_query(query):
    """
    Very small parser for a limited SQL‑like syntax.
    Supported form:
        SELECT <cols> [WHERE <condition>] [ORDER BY <col> [ASC|DESC]]
    """
    pattern = r'''
        ^\s*SELECT\s+(?P<select>[\w\*,\s]+)
        (?:\s+WHERE\s+(?P<where>[^;]+?))?
        (?:\s+ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?)?
        \s*;?\s*$
    '''
    m = re.match(pattern, query, re.IGNORECASE | re.VERBOSE)
    if not m:
        raise ValueError("Query format is invalid")

    select_part = [c.strip() for c in m.group('select').split(',')]
    where_part = m.group('where')
    order_col = m.group('order')
    order_dir = m.group('dir')

    return select_part, where_part, order_col, order_dir

def _parse_condition(cond_str):
    """
    Parses a simple condition of the form <column> <operator> <value>
    """
    cond_pattern = r'^\s*(?P<col>\w+)\s*(?P<op>[=!<>]=?|[<>])\s*(?P<val>.+?)\s*$'
    m = re.match(cond_pattern, cond_str)
    if not m:
        raise ValueError("WHERE clause format is invalid")

    col = m.group('col')
    op_token = m.group('op')
    val_raw = m.group('val').strip()

    # Strip surrounding quotes for string literals
    if (val_raw.startswith("'") and val_raw.endswith("'")) or \
       (val_raw.startswith('"') and val_raw.endswith('"')):
        value = val_raw[1:-1]
    else:
        # Try to interpret as number
        try:
            if '.' in val_raw:
                value = float(val_raw)
            else:
                value = int(val_raw)
        except ValueError:
            # treat as literal string
            value = val_raw

    if op_token not in _OPERATOR_MAP:
        raise ValueError(f"Unsupported operator '{op_token}'")

    op_func = _OPERATOR_MAP[op_token]

    def condition(row):
        # Missing key is treated as None
        left = row.get(col, None)
        return op_func(left, value)

    return condition

def run_custom_query(dataset, query):
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    query : str
        SQL‑like statement.

    Returns
    -------
    list[dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    for rec in dataset:
        if not isinstance(rec, dict):
            raise ValueError("All items in the dataset must be dictionaries")

    select_cols, where_str, order_col, order_dir = _parse_query(query)

    # Handle SELECT *
    if len(select_cols) == 1 and select_cols[0] == '*':
        selected = lambda row: dict(row)
    else:
        for col in select_cols:
            if not all(col in r for r in dataset):
                # allow missing keys but warn
                pass

        def selected(row):
            return {c: row.get(c, None) for c in select_cols}

    # Apply WHERE clause
    if where_str:
        cond_func = _parse_condition(where_str)
        filtered = filter(cond_func, dataset)
    else:
        filtered = dataset

    # Apply ORDER BY
    if order_col:
        reverse = (order_dir and order_dir.upper() == 'DESC')
        try:
            sorted_data = sorted(filtered, key=lambda r: (r.get(order_col) is None, r.get(order_col)), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot order by column '{order_col}': {exc}") from exc
    else:
        sorted_data = list(filtered)

    # Apply SELECT projection
    result = [selected(row) for row in sorted_data]
    return result
import re
import operator
from functools import reduce

# Map of supported operators
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Map of logical operators
_LOGICAL_MAP = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}


def _parse_condition(cond_str):
    """
    Very small parser that turns a simple WHERE condition into a callable.
    Supports comparisons and AND/OR chaining with no parentheses.
    """
    # Tokenize by space
    tokens = cond_str.strip().split()
    if not tokens:
        return lambda rec: True

    # Build a list of functions for each comparison
    funcs = []
    i = 0
    while i < len(tokens):
        # Expect: field op value
        if i + 2 >= len(tokens):
            raise ValueError(f"Malformed condition near: {' '.join(tokens[i:])}")

        field, op_token, value_token = tokens[i], tokens[i + 1], tokens[i + 2]
        if op_token not in _OP_MAP:
            raise ValueError(f"Unsupported operator '{op_token}' in condition")

        # Try to interpret the value as int/float, else strip quotes
        try:
            value = float(value_token) if '.' in value_token else int(value_token)
        except ValueError:
            # strip surrounding quotes if any
            value = value_token.strip("'\"")

        op_func = _OP_MAP[op_token]
        funcs.append((field, op_func, value))

        i += 3
        if i < len(tokens):
            logical = tokens[i].upper()
            if logical not in _LOGICAL_MAP:
                raise ValueError(f"Unsupported logical operator '{logical}'")
            funcs.append(_LOGICAL_MAP[logical])
            i += 1

    def condition(record):
        # Evaluate chained comparisons
        it = iter(funcs)
        result = None
        for item in it:
            if isinstance(item, tuple):
                field, op_func, val = item
                # Missing field -> treat as None
                rec_val = record.get(field, None)
                cmp_res = op_func(rec_val, val)
                result = cmp_res if result is None else _LOGICAL_MAP[prev_logic](result, cmp_res)
            else:
                prev_logic = item
        return result if result is not None else True

    return condition


def _parse_query(query):
    """
    Very small SQL-like parser.
    Supported syntax:
        SELECT <cols> [WHERE <condition>] [ORDER BY <col> ASC|DESC]
    """
    # Normalize whitespace
    q = re.sub(r'\s+', ' ', query.strip())
    if not q.upper().startswith('SELECT'):
        raise ValueError("Query must start with SELECT")

    # Extract parts
    select_part = q[6:].strip()  # after SELECT
    where_match = re.search(r'\bWHERE\b', select_part, flags=re.IGNORECASE)
    order_match = re.search(r'\bORDER BY\b', select_part, flags=re.IGNORECASE)

    # Determine boundaries
    where_start = where_match.start() if where_match else len(select_part)
    order_start = order_match.start() if order_match else len(select_part)

    cols_str = select_part[:where_start].strip()
    where_clause = None
    order_by_clause = None

    if where_match:
        where_end = order_start if order_match else len(select_part)
        where_clause = select_part[where_start + 5:where_end].strip()  # after WHERE

    if order_match:
        order_by_clause = select_part[order_start + 9:].strip()  # after ORDER BY

    cols = [c.strip() for c in cols_str.split(',')] if cols_str else []
    if not cols or cols == ['*']:
        cols = None  # Means all columns

    return cols, where_clause, order_by_clause


def run_custom_query(dataset, query):
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        List of records, each a dictionary.
    query : str
        Query string supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Resulting records after applying the query.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    cols, where_clause, order_by_clause = _parse_query(query)

    # Filter
    if where_clause:
        cond_func = _parse_condition(where_clause)
        filtered = [rec for rec in dataset if cond_func(rec)]
    else:
        filtered = list(dataset)

    # Order
    if order_by_clause:
        parts = order_by_clause.split()
        if len(parts) not in (1, 2):
            raise ValueError("ORDER BY clause must be 'column [ASC|DESC]'")
        order_col = parts[0]
        reverse = False
        if len(parts) == 2:
            dir_token = parts[1].upper()
            if dir_token not in ('ASC', 'DESC'):
                raise ValueError("ORDER BY direction must be ASC or DESC")
            reverse = dir_token == 'DESC'
        try:
            filtered.sort(key=lambda rec: rec.get(order_col), reverse=reverse)
        except TypeError:
            # Mixed types; fallback to string comparison
            filtered.sort(key=lambda rec: str(rec.get(order_col)), reverse=reverse)

    # Project columns
    if cols is not None:
        result = [{c: rec.get(c) for c in cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
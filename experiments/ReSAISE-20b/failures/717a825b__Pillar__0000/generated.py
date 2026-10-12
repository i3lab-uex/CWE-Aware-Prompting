import re
import operator
from functools import reduce

# Supported comparison operators mapping
_COMPARISONS = {
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge,
    '<': operator.lt,
    '>': operator.gt,
}

# Supported logical operators mapping
_LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# Regular expression patterns for parsing
_SELECT_RE = re.compile(r'SELECT\s+(?P<columns>[\*\w,\s]+)', re.IGNORECASE)
_WHERE_RE = re.compile(r'WHERE\s+(?P<conditions>.+?)\s*(ORDER BY|$)', re.IGNORECASE | re.DOTALL)
_ORDERBY_RE = re.compile(r'ORDER\s+BY\s+(?P<column>\w+)(\s+(ASC|DESC))?', re.IGNORECASE)

# Regular expression for a single condition
_COND_RE = re.compile(
    r'(?P<left>\w+)\s*(?P<op>==|!=|<=|>=|<|>)\s*(?P<right>.+?)',
    re.IGNORECASE
)

# Regular expression for splitting logical operators
_LOGICAL_SPLIT_RE = re.compile(r'\s+(AND|OR)\s+', re.IGNORECASE)


def _parse_select(query: str):
    m = _SELECT_RE.search(query)
    if not m:
        raise ValueError("Missing or malformed SELECT clause")
    cols = [c.strip() for c in m.group('columns').split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return None  # means all columns
    return cols


def _parse_where(query: str):
    m = _WHERE_RE.search(query)
    if not m:
        return None
    cond_str = m.group('conditions').strip()
    # Split into tokens: conditions and logical operators
    parts = _LOGICAL_SPLIT_RE.split(cond_str)
    # parts will be like [cond1, 'AND', cond2, ...]
    return parts


def _parse_orderby(query: str):
    m = _ORDERBY_RE.search(query)
    if not m:
        return None
    column = m.group('column')
    order = m.group(3)
    reverse = True if order and order.upper() == 'DESC' else False
    return column, reverse


def _eval_condition(row: dict, cond_str: str):
    """Evaluate a single simple condition against a row."""
    m = _COND_RE.fullmatch(cond_str.strip())
    if not m:
        raise ValueError(f"Invalid condition: {cond_str!r}")
    left = m.group('left')
    op_sym = m.group('op')
    right_raw = m.group('right').strip()

    if left not in row:
        raise ValueError(f"Column {left!r} does not exist in data")

    left_val = row[left]
    # Try to interpret right value as number or string
    try:
        right_val = float(right_raw) if '.' in right_raw else int(right_raw)
    except ValueError:
        # Remove surrounding quotes if present
        right_val = right_raw.strip('\'"')

    comp_op = _COMPARISONS[op_sym]
    return comp_op(left_val, right_val)


def execute_custom_query(data: list[dict], query: str) -> list[dict]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> [ASC|DESC]]

    - <columns> is a comma separated list of keys or '*' for all.
    - <condition> can contain simple comparisons (==, !=, <, <=, >, >=)
      combined with AND / OR.
    - ORDER BY sorts the result by a single column, default ASC.

    Parameters
    ----------
    data : list[dict]
        Dataset to query.
    query : str
        SQL-like query string.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or refers to non‑existent columns.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries")

    # Normalize whitespace
    q = ' '.join(query.strip().split())

    # Parse SELECT
    selected_cols = _parse_select(q)

    # Parse WHERE
    where_parts = _parse_where(q)

    # Apply filtering
    def row_matches(row):
        if where_parts is None:
            return True
        # Evaluate left-to-right with logical operators
        it = iter(where_parts)
        result = _eval_condition(row, next(it))
        for token in it:
            op_token = token.upper()
            if op_token not in _LOGICAL:
                raise ValueError(f"Unsupported logical operator: {token!r}")
            next_cond = _eval_condition(row, next(it))
            result = _LOGICAL[op_token](result, next_cond)
        return result

    filtered = [r for r in data if row_matches(r)]

    # Parse ORDER BY
    orderby = _parse_orderby(q)
    if orderby:
        col, reverse = orderby
        try:
            filtered.sort(key=lambda r: r[col], reverse=reverse)
        except KeyError:
            raise ValueError(f"ORDER BY column {col!r} does not exist")

    # Apply SELECT projection
    if selected_cols is None:
        return filtered

    projected = []
    for r in filtered:
        try:
            projected.append({c: r[c] for c in selected_cols})
        except KeyError as exc:
            raise ValueError(f"Selected column {exc.args[0]!r} not found in data") from None

    return projected
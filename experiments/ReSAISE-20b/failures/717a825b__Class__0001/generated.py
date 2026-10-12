import re
import operator
from functools import reduce

# Supported comparison operators and their corresponding functions
_COMPARISON_OPERATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Supported logical operators
_LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# Regular expression patterns for parsing
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<columns>[\*\w,\s]+)          # SELECT columns
    \s+WHERE\s+(?P<where>.+?)                    # WHERE clause
    (\s+ORDER\s+BY\s+(?P<order>\w+)(\s+(ASC|DESC))?)?   # optional ORDER BY
    \s*;?\s*$                                    # optional semicolon and trailing spaces
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Tokenize a simple boolean expression in the WHERE clause
_TOKEN_RE = re.compile(
    r"""
    (?P<identifier>\w+)
    \s*
    (?P<operator>==|=|>=|<=|>|<)
    \s*
    (?P<value>'[^']*'|"[^"]*"|\d+(\.\d+)?)
    |(?P<logical>AND|OR)
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _parse_value(token: str):
    """Convert a string token to an int, float or stripped string."""
    if token.startswith(("'", '"')) and token.endswith(("'", '"')):
        return token[1:-1]
    try:
        if '.' in token:
            return float(token)
        return int(token)
    except ValueError:
        raise ValueError(f"Invalid literal in WHERE clause: {token}")

def _evaluate_where(record, tokens):
    """Evaluate the tokenized WHERE expression against a single record."""
    stack = []
    for tok in tokens:
        if tok['logical']:
            op_func = _LOGICAL_OPERATORS[tok['logical'].upper()]
            right = stack.pop()
            left = stack.pop()
            stack.append(op_func(left, right))
        else:
            key = tok['identifier']
            if key not in record:
                raise ValueError(f"Field '{key}' not found in data.")
            comp_func = _COMPARISON_OPERATORS[tok['operator']]
            val = _parse_value(tok['value'])
            stack.append(comp_func(record[key], val))
    if len(stack) != 1:
        raise ValueError("Malformed WHERE clause.")
    return stack[0]

def execute_custom_query(data, query):
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    data : list[dict]
        The dataset to query.
    query : str
        A SQL‑like query string. Supports:
          SELECT <columns> WHERE <condition> [ORDER BY <column> [ASC|DESC]];

    Returns
    -------
    list[dict]
        The filtered and ordered result set.

    Raises
    ------
    ValueError
        If the query is syntactically invalid or cannot be executed.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries.")

    match = _QUERY_RE.match(query)
    if not match:
        raise ValueError("Query syntax is invalid.")

    columns_str = match.group('columns')
    where_clause = match.group('where')
    order_col = match.group('order')
    order_dir = match.group(5)  # ASC or DESC

    # Parse selected columns
    if columns_str.strip() == '*':
        select_cols = None  # all columns
    else:
        select_cols = [c.strip() for c in columns_str.split(',')]
        if not all(select_cols):
            raise ValueError("Invalid column list in SELECT clause.")

    # Tokenize WHERE clause
    tokens = []
    for m in _TOKEN_RE.finditer(where_clause):
        token_dict = {}
        if m.group('identifier'):
            token_dict['identifier'] = m.group('identifier')
            token_dict['operator'] = m.group('operator')
            token_dict['value'] = m.group('value')
        elif m.group('logical'):
            token_dict['logical'] = m.group('logical')
        else:
            continue
        tokens.append(token_dict)
    if not tokens:
        raise ValueError("WHERE clause is empty or invalid.")

    # Filter data
    filtered = [rec for rec in data if _evaluate_where(rec, tokens)]

    # Order data
    if order_col:
        reverse = (order_dir and order_dir.upper() == 'DESC')
        try:
            filtered.sort(key=lambda r: r.get(order_col, None), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by column '{order_col}': {e}")

    # Project columns
    if select_cols is not None:
        result = [{k: rec[k] for k in select_cols if k in rec} for rec in filtered]
    else:
        result = [rec.copy() for rec in filtered]

    return result
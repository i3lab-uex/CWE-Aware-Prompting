import re
import operator
from functools import reduce

# Mapping of supported comparison operators to actual functions
_COMPARATORS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Supported logical connectors
_LOGICALS = {
    'AND': lambda a, b: a and b,
    'OR':  lambda a, b: a or b
}


def _parse_select_clause(query):
    """Parse SELECT clause and return list of fields (or ['*'])."""
    match = re.search(r'^SELECT\s+(?P<fields>[\*\w,\s]+)', query, re.IGNORECASE)
    if not match:
        raise ValueError("Missing or malformed SELECT clause")
    fields = [f.strip() for f in match.group('fields').split(',')]
    if fields == ['*']:
        return None  # Means all fields
    return fields


def _parse_where_clause(query):
    """Parse WHERE clause into a function that evaluates a record."""
    match = re.search(r'\bWHERE\b(?P<cond>.+?)(?:\bORDER\s+BY\b|$)', query, re.IGNORECASE | re.DOTALL)
    if not match:
        return lambda rec: True  # No WHERE -> always true

    cond_str = match.group('cond').strip()

    # Tokenize simple expressions: field op value (value may be quoted string or number)
    token_re = re.compile(
        r"""(?P<field>\w+)\s*
            (?P<op>=|==|!=|<>|>|<|>=|<=)\s*
            (?P<value>
                '(?:\\'|[^'])*' |    # single quoted string
                "(?:\\"|[^"])*" |    # double quoted string
                \d+(?:\.\d+)?         # number
            )""",
        re.VERBOSE | re.IGNORECASE
    )

    def _convert_value(v):
        v = v.strip()
        if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
            return v[1:-1].replace("\\'", "'").replace('\\"', '"')
        try:
            if '.' in v:
                return float(v)
            return int(v)
        except ValueError:
            raise ValueError(f"Unsupported value format: {v}")

    # Build a list of (field, op_func, value) tuples
    parts = []
    pos = 0
    while pos < len(cond_str):
        m = token_re.match(cond_str, pos)
        if not m:
            raise ValueError(f"Invalid condition near: {cond_str[pos:]}")
        field = m.group('field')
        op_sym = m.group('op')
        val_raw = m.group('value')
        op_func = _COMPARATORS.get(op_sym)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_sym}")
        val = _convert_value(val_raw)
        parts.append((field, op_func, val))
        pos = m.end()

        # Handle logical connectors
        conn_match = re.match(r'\s*(AND|OR)\s*', cond_str[pos:], re.IGNORECASE)
        if conn_match:
            parts.append(conn_match.group(1).upper())
            pos += conn_match.end()

    # Build a lambda that evaluates the condition
    def cond_func(rec):
        stack = []
        for part in parts:
            if isinstance(part, tuple):  # a condition
                field, op_func, val = part
                if field not in rec:
                    raise ValueError(f"Field {field} not found in record")
                stack.append(op_func(rec[field], val))
            else:  # logical operator
                if len(stack) < 2:
                    raise ValueError("Malformed WHERE clause")
                b = stack.pop()
                a = stack.pop()
                logical_func = _LOGICALS[part]
                stack.append(logical_func(a, b))
        if len(stack) != 1:
            raise ValueError("Malformed WHERE clause")
        return stack[0]

    return cond_func


def _parse_order_by_clause(query):
    """Parse ORDER BY clause and return list of (field, asc/desc)."""
    match = re.search(r'\bORDER\s+BY\b(?P<order>.+)', query, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    order_str = match.group('order').strip()
    fields = []
    for part in re.split(r',\s*', order_str):
        tokens = part.strip().split()
        field = tokens[0]
        direction = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Invalid ORDER BY direction: {direction}")
        fields.append((field, direction == 'DESC'))
    return fields


def execute_user_query(records, user_query):
    """
    Execute a simple SQL-like query on a list of dictionary records.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    user_query : str
        Query string supporting SELECT, WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        The resulting records after applying the query.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("All items in records must be dictionaries")

    # Normalize whitespace
    query = re.sub(r'\s+', ' ', user_query.strip())

    try:
        select_fields = _parse_select_clause(query)
        where_func = _parse_where_clause(query)
        order_by = _parse_order_by_clause(query)

        # Filter records
        filtered = [rec for rec in records if where_func(rec)]

        # Sort if needed
        if order_by:
            def sort_key(rec):
                return tuple(
                    rec.get(field, None) if not desc else _invert_value(rec.get(field, None))
                    for field, desc in order_by
                )
            filtered.sort(key=sort_key)

        # Project fields
        if select_fields is None:
            result = filtered
        else:
            result = [{k: rec.get(k, None) for k in select_fields} for rec in filtered]

        return result
    except Exception as exc:
        raise ValueError(f"Query execution failed: {exc}") from exc


def _invert_value(v):
    """Helper to invert order for DESC sorting."""
    # For numbers, use negative; for others, rely on reverse sort via tuple
    if isinstance(v, (int, float)):
        return -v
    # For strings and others, use a wrapper that reverses comparison
    class _Rev:
        def __init__(self, val):
            self.val = val

        def __lt__(self, other):
            return self.val > other.val
    return _Rev(v)
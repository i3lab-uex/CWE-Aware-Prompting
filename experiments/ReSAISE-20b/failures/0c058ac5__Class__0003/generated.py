import re
import operator
from functools import reduce

# Mapping of supported comparison operators to functions
_COMPARISONS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Supported logical operators
_LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# Regex patterns for parsing
SELECT_PATTERN = re.compile(r'^\s*SELECT\s+(?P<fields>[\*\w,\s]+)\s+WHERE\s+(?P<where>.+?)\s*(ORDER\s+BY\s+(?P<order>[\w,\s]+))?\s*$', re.IGNORECASE)
WHERE_CONDITION_PATTERN = re.compile(
    r'(?P<field>\w+)\s*(?P<op>[=<>!]+|==|!=)\s*'
    r'(?P<value>(?:\'[^\']*\'|"[^"]*"|\d+(\.\d+)?))',
    re.IGNORECASE
)
ORDER_PATTERN = re.compile(r'(?P<field>\w+)\s*(?P<direction>ASC|DESC)?', re.IGNORECASE)

def _parse_value(raw):
    """Convert a raw SQL value string to Python type."""
    if raw.startswith(("'", '"')) and raw.endswith(("'", '"')):
        return raw[1:-1]
    try:
        if '.' in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        raise ValueError(f"Invalid literal value: {raw}")

def _build_where_func(where_clause):
    """Return a function that evaluates the WHERE clause for a record."""
    tokens = []
    pos = 0
    while pos < len(where_clause):
        m = WHERE_CONDITION_PATTERN.match(where_clause, pos)
        if not m:
            raise ValueError(f"Invalid WHERE clause near: '{where_clause[pos:]}'")
        field, op_sym, raw_val = m.group('field'), m.group('op'), m.group('value')
        op_func = _COMPARISONS.get(op_sym)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_sym}")
        val = _parse_value(raw_val)

        def condition(record, f=field, op=op_func, v=val):
            return op(record.get(f), v)

        tokens.append(condition)
        pos = m.end()

        # Skip optional logical operator
        while pos < len(where_clause) and where_clause[pos].isspace():
            pos += 1
        if pos >= len(where_clause):
            break

        # Logical operator
        for log_op in _LOGICAL_OPERATORS:
            if where_clause[pos:pos+len(log_op)].upper() == log_op:
                tokens.append(_LOGICAL_OPERATORS[log_op])
                pos += len(log_op)
                break
        else:
            raise ValueError(f"Unsupported logical operator near: '{where_clause[pos:]}'")

    def evaluator(record):
        stack = []
        for token in tokens:
            if callable(token):
                stack.append(token(record))
            else:  # logical operator
                if len(stack) < 2:
                    raise ValueError("Malformed WHERE clause")
                b = stack.pop()
                a = stack.pop()
                stack.append(token(a, b))
        if len(stack) != 1:
            raise ValueError("Malformed WHERE clause")
        return stack[0]

    return evaluator

def _build_order_func(order_clause):
    """Return a key function for sorting and reverse flag."""
    parts = [p.strip() for p in order_clause.split(',')]
    orders = []
    for part in parts:
        m = ORDER_PATTERN.match(part)
        if not m:
            raise ValueError(f"Invalid ORDER BY clause: '{part}'")
        field = m.group('field')
        direction = m.group('direction') or 'ASC'
        reverse = direction.upper() == 'DESC'
        orders.append((field, reverse))
    def key_func(record):
        return tuple(
            record.get(field)
            for field, _ in orders
        )
    reverse = any(r for _, r in orders)
    return key_func, reverse

def submit_user_query(records: list[dict], sql_statement: str) -> list[dict]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supports SELECT, WHERE and ORDER BY clauses.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")
    if not isinstance(sql_statement, str):
        raise ValueError("sql_statement must be a string")

    m = SELECT_PATTERN.match(sql_statement)
    if not m:
        raise ValueError("Invalid SQL statement format")

    fields_raw = [f.strip() for f in m.group('fields').split(',')]
    all_fields = fields_raw == ['*']

    where_clause = m.group('where')
    order_clause = m.group('order')

    try:
        where_func = _build_where_func(where_clause)
    except ValueError as e:
        raise ValueError(f"WHERE clause error: {e}") from None

    try:
        if order_clause:
            key_func, reverse = _build_order_func(order_clause)
        else:
            key_func, reverse = None, False
    except ValueError as e:
        raise ValueError(f"ORDER BY clause error: {e}") from None

    # Filter records
    filtered = [rec for rec in records if where_func(rec)]

    # Sort if needed
    if key_func:
        try:
            filtered.sort(key=key_func, reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Sorting error: {e}") from None

    # Project fields
    if all_fields:
        result = [dict(rec) for rec in filtered]
    else:
        missing = set(fields_raw) - {k for d in filtered for k in d}
        if missing:
            raise ValueError(f"Requested field(s) not found: {', '.join(missing)}")
        result = [{k: rec.get(k) for k in fields_raw} for rec in filtered]

    return result
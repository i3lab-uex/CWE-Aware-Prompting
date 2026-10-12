import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Map string operators to actual functions
OPERATORS = {
    '=': eq,
    '!=': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(r'\s*SELECT\s+(?P<select>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
WHERE_RE = re.compile(r'\s*WHERE\s+(?P<where>.+)', re.IGNORECASE)
ORDER_BY_RE = re.compile(r'\s*ORDER\s+BY\s+(?P<order>\w+)\s*(?P<dir>ASC|DESC)?', re.IGNORECASE)

# Simple condition parser
COND_RE = re.compile(
    r'(?P<field>\w+)\s*(?P<op>=|!=|<=|<|>=|>)\s*'
    r'(?P<value>\d+(\.\d+)?|\'[^\']*\'|"[^"]*")',
    re.IGNORECASE
)

def _parse_condition(cond_str):
    """Parse a single condition string into a callable."""
    match = COND_RE.fullmatch(cond_str.strip())
    if not match:
        raise ValueError(f"Invalid condition: {cond_str!r}")
    field = match.group('field')
    op = OPERATORS[match.group('op')]
    raw_value = match.group('value')

    # Convert value to int/float or strip quotes
    if raw_value.isdigit():
        value = int(raw_value)
    else:
        try:
            value = float(raw_value)
        except ValueError:
            # Strip surrounding quotes
            if (raw_value.startswith("'") and raw_value.endswith("'")) or \
               (raw_value.startswith('"') and raw_value.endswith('"')):
                value = raw_value[1:-1]
            else:
                raise ValueError(f"Unable to parse value: {raw_value!r}")

    def condition(record):
        if field not in record:
            raise ValueError(f"Field {field!r} not found in record")
        return op(record[field], value)

    return condition

def _parse_where(where_str):
    """Parse the WHERE clause into a single callable."""
    # Split by AND/OR (case-insensitive)
    tokens = re.split(r'\s+(AND|OR)\s+', where_str, flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Build list of conditions and operators
    conditions = []
    ops = []

    for token in tokens:
        tok_upper = token.upper()
        if tok_upper == 'AND':
            ops.append('and')
        elif tok_upper == 'OR':
            ops.append('or')
        else:
            conditions.append(_parse_condition(token))

    if not conditions:
        raise ValueError("No valid conditions in WHERE clause")

    def combined(record):
        # Evaluate left to right
        result = conditions[0](record)
        for op, cond in zip(ops, conditions[1:]):
            if op == 'and':
                result = result and cond(record)
            else:
                result = result or cond(record)
        return result

    return combined

def _parse_select(select_str):
    """Return list of fields to project."""
    select_str = select_str.strip()
    if select_str == '*':
        return None  # Means all fields
    fields = [f.strip() for f in select_str.split(',')]
    if not all(fields):
        raise ValueError("Empty field name in SELECT clause")
    return fields

def _parse_order_by(order_str):
    """Return field and direction for ordering."""
    if not order_str:
        return None, None
    match = ORDER_BY_RE.match(order_str)
    if not match:
        raise ValueError("Malformed ORDER BY clause")
    field = match.group('order')
    direction = match.group('dir') or 'ASC'
    return field, direction.upper()

def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    sql_command : str
        SQL-like command string.

    Returns
    -------
    list[dict]
        Result set after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or evaluation fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("Each record must be a dictionary")

    # Normalize whitespace and split into clauses
    cmd = sql_command.strip()
    if not cmd.lower().startswith('select'):
        raise ValueError("Only SELECT queries are supported")

    # Extract SELECT part
    select_match = SELECT_RE.match(cmd)
    if not select_match:
        raise ValueError("Malformed SELECT clause")
    fields = _parse_select(select_match.group('select'))

    # Extract WHERE part if present
    where_clause = None
    remaining = cmd[select_match.end():]
    where_match = WHERE_RE.search(remaining)
    if where_match:
        where_clause = _parse_where(where_match.group('where'))
        remaining = remaining[where_match.end():]

    # Extract ORDER BY part if present
    order_field, order_dir = None, None
    order_match = ORDER_BY_RE.search(remaining)
    if order_match:
        order_field, order_dir = _parse_order_by(order_match.group(0))

    # Apply filtering
    if where_clause:
        try:
            filtered = [r for r in records if where_clause(r)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}") from e
    else:
        filtered = records[:]

    # Apply ordering
    if order_field:
        try:
            reverse = (order_dir == 'DESC')
            filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error sorting by {order_field!r}: {e}") from e

    # Apply projection
    if fields is not None:
        result = [{k: r.get(k) for k in fields} for r in filtered]
    else:
        result = [dict(r) for r in filtered]  # shallow copy

    return result
import re
import operator
from functools import cmp_to_key

# Supported operators mapping
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regex patterns for parsing the SQL‑like statement
SELECT_RE = re.compile(r'\s*select\s+(?P<cols>[\w\*,\s]+)', re.I)
WHERE_RE = re.compile(r'\s*where\s+(?P<cond>.+)', re.I)
ORDER_BY_RE = re.compile(r'\s*order\s+by\s+(?P<field>\w+)(\s+(?P<dir>asc|desc))?', re.I)

def _parse_columns(select_part: str):
    cols = [c.strip() for c in select_part.split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return None  # all columns
    for c in cols:
        if not re.match(r'^\w+$', c):
            raise ValueError(f"Invalid column name: {c}")
    return cols

def _parse_condition(cond_part: str):
    # Very simple condition parser: field operator value
    for op_sym in sorted(OPERATORS.keys(), key=len, reverse=True):
        if op_sym in cond_part:
            field, value = map(str.strip, cond_part.split(op_sym, 1))
            if not re.match(r'^\w+$', field):
                raise ValueError(f"Invalid field in WHERE clause: {field}")
            # Try to interpret value as int or float, else keep string
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                # strip quotes if present
                value = re.sub(r"^'(.*)'$|^\"(.*)\"$", r'\1\2', value)
            return field, OPERATORS[op_sym], value
    raise ValueError(f"Unsupported or malformed WHERE condition: {cond_part}")

def _parse_order_by(order_part: str):
    match = ORDER_BY_RE.match(order_part)
    if not match:
        raise ValueError(f"Malformed ORDER BY clause: {order_part}")
    field = match.group('field')
    direction = match.group('dir') or 'asc'
    return field, direction.lower()

def submit_user_query(records: list[dict], sql_statement: str) -> list[dict]:
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Dataset to query.
    sql_statement : str
        Query string. Example:
            "SELECT name, age WHERE age >= 30 ORDER BY name DESC"

    Returns
    -------
    list[dict]
        Resulting records after SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # 1. SELECT
    select_match = SELECT_RE.match(sql_statement)
    if not select_match:
        raise ValueError("Missing or malformed SELECT clause")
    cols = _parse_columns(select_match.group('cols'))

    remaining = sql_statement[select_match.end():]

    # 2. WHERE (optional)
    where_clause = None
    order_by_clause = None

    # Check for ORDER BY first (to split remaining)
    order_match = ORDER_BY_RE.search(remaining)
    if order_match:
        where_part = remaining[:order_match.start()]
        order_by_clause = remaining[order_match.start():]
    else:
        where_part = remaining

    if where_part.strip():
        # look for WHERE
        where_match = WHERE_RE.search(where_part)
        if not where_match:
            raise ValueError("Malformed WHERE clause")
        field, op_func, value = _parse_condition(where_match.group('cond'))
        where_clause = (field, op_func, value)

    # 3. ORDER BY
    if order_by_clause:
        field_order, direction = _parse_order_by(order_by_clause)
    else:
        field_order, direction = None, None

    # Apply WHERE
    filtered = records
    if where_clause:
        field, op_func, value = where_clause
        try:
            filtered = [r for r in records if op_func(r.get(field), value)]
        except Exception as exc:
            raise ValueError(f"Error applying WHERE clause: {exc}") from exc

    # Apply ORDER BY
    if field_order:
        try:
            reverse = direction == 'desc'
            filtered.sort(key=lambda r: r.get(field_order), reverse=reverse)
        except Exception as exc:
            raise ValueError(f"Error applying ORDER BY clause: {exc}") from exc

    # Apply SELECT
    if cols is not None:
        result = [{k: v for k, v in r.items() if k in cols} for r in filtered]
    else:
        result = [r.copy() for r in filtered]

    return result
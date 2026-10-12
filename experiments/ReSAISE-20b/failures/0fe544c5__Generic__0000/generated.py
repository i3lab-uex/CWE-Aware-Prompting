import re
from operator import eq, ne, lt, le, gt, ge
from functools import reduce

# Mapping of string operators to functions
OPERATORS = {
    '=': eq,
    '!=': ne,
    '<': lt,
    '<=': le,
    '>': gt,
    '>=': ge
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(r'\s*SELECT\s+(?P<cols>[\*\w,\s]+)', re.IGNORECASE)
WHERE_RE = re.compile(r'\s+WHERE\s+(?P<cond>.+?)', re.IGNORECASE)
ORDER_BY_RE = re.compile(r'\s+ORDER\s+BY\s+(?P<order>[\w,\s]+)', re.IGNORECASE)

# Simple condition parser: supports "field op value" with AND/OR
COND_RE = re.compile(r'(?P<field>\w+)\s*(?P<op>=|!=|<=|<|>=|>)\s*(?P<value>[^ ]+)', re.IGNORECASE)
LOGICAL_RE = re.compile(r'\s+(AND|OR)\s+', re.IGNORECASE)


def _parse_query(sql: str):
    """Parse the SQL-like query into components."""
    sql = sql.strip()
    # SELECT
    m = SELECT_RE.match(sql)
    if not m:
        raise ValueError('Missing or malformed SELECT clause')
    cols = [c.strip() for c in m.group('cols').split(',')]
    if len(cols) == 1 and cols[0] == '*':
        select_cols = None
    else:
        select_cols = cols

    # Remaining part after SELECT
    rest = sql[m.end():]

    # WHERE (optional)
    where_clause = None
    m_where = WHERE_RE.search(rest)
    if m_where:
        where_clause = m_where.group('cond')
        rest = rest[:m_where.start()] + rest[m_where.end():]

    # ORDER BY (optional)
    order_by = None
    m_order = ORDER_BY_RE.search(rest)
    if m_order:
        order_by = [c.strip() for c in m_order.group('order').split(',')]

    return select_cols, where_clause, order_by


def _build_condition(cond_str: str):
    """Build a function that evaluates the condition on a record."""
    # Split by AND/OR
    parts = LOGICAL_RE.split(cond_str)
    ops = LOGICAL_RE.findall(cond_str)

    # Build a list of lambda for each simple condition
    cond_funcs = []
    for part in parts:
        m = COND_RE.fullmatch(part.strip())
        if not m:
            raise ValueError(f'Invalid condition: {part}')
        field, op_sym, value_raw = m.group('field', 'op', 'value')
        op_func = OPERATORS[op_sym]
        # Try to convert value to int or float, otherwise keep as string
        try:
            if '.' in value_raw:
                value = float(value_raw)
            else:
                value = int(value_raw)
        except ValueError:
            # Strip quotes if present
            value = value_raw.strip("'\"")
        cond_funcs.append((field, op_func, value))

    def eval_record(rec):
        # Evaluate first condition
        field, func, val = cond_funcs[0]
        res = func(rec.get(field), val)
        # Apply logical operators
        for i, op in enumerate(ops):
            field, func, val = cond_funcs[i + 1]
            cur = func(rec.get(field), val)
            if op.upper() == 'AND':
                res = res and cur
            else:  # OR
                res = res or cur
        return res

    return eval_record


def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    sql_command : str
        The SQL-like command.

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError('records must be a list')
    if not all(isinstance(r, dict) for r in records):
        raise ValueError('Each record must be a dictionary')

    try:
        select_cols, where_clause, order_by = _parse_query(sql_command)
    except Exception as e:
        raise ValueError(f'Failed to parse query: {e}') from e

    # Filter records
    if where_clause:
        try:
            cond_func = _build_condition(where_clause)
        except Exception as e:
            raise ValueError(f'Invalid WHERE clause: {e}') from e
        filtered = [rec for rec in records if cond_func(rec)]
    else:
        filtered = list(records)

    # Order by
    if order_by:
        try:
            filtered.sort(key=lambda r: tuple(r.get(k) for k in order_by))
        except Exception as e:
            raise ValueError(f'ORDER BY error: {e}') from e

    # Project columns
    if select_cols is None:
        result = filtered
    else:
        result = []
        for rec in filtered:
            projected = {k: rec.get(k) for k in select_cols}
            result.append(projected)

    return result
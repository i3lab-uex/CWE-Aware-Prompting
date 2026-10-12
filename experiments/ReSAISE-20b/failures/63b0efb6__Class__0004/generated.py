import re
from operator import eq, ne, lt, le, gt, ge
from functools import partial

# Map string operators to functions
_OPERATOR_MAP = {
    '==': eq,
    '=':  eq,   # allow single equals
    '!=': ne,
    '<':  lt,
    '<=': le,
    '>':  gt,
    '>=': ge
}

# Regular expressions for parsing the command
_RE_SELECT = re.compile(r'\s*SELECT\s+(?P<fields>[\*\w,\s]+)\s+WHERE\s+(?P<where>.+)', re.IGNORECASE)
_RE_ORDER = re.compile(r'\s*ORDER\s+BY\s+(?P<field>\w+)(?:\s+(?P<dir>ASC|DESC))?\s*$', re.IGNORECASE)
_RE_SIMPLE_COND = re.compile(
    r'(?P<field>\w+)\s*(?P<op>==|!=|>=|<=|>|<|=)\s*(?P<value>.+)',
    re.IGNORECASE
)

def _parse_value(val: str):
    """Try to interpret the value as int, float or strip quotes."""
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Try numeric conversion
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        pass
    # Fallback: string without quotes
    return val

def _evaluate_condition(record, field, op_func, value):
    """Return True if record satisfies the condition."""
    try:
        record_value = record[field]
    except KeyError:
        raise ValueError(f"Field '{field}' not found in record")
    return op_func(record_value, value)

def run_sql_query(records: list[dict], command: str) -> list[dict]:
    """
    Execute a very small subset of SQL-like commands on an in-memory dataset.
    
    Supported syntax:
        SELECT <fields> WHERE <field> <op> <value> [ORDER BY <field> [ASC|DESC]]
    
    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    command : str
        The SQL-like statement.

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the command is malformed or cannot be executed.
    """
    if not records:
        return []

    # Step 1: Parse SELECT and WHERE
    m_select = _RE_SELECT.match(command)
    if not m_select:
        raise ValueError("Command must start with SELECT and contain WHERE")

    fields_str = m_select.group('fields')
    where_clause = m_select.group('where')

    # Step 2: Parse ORDER BY (optional)
    order_field = None
    order_dir = 'ASC'
    m_order = _RE_ORDER.search(where_clause)
    if m_order:
        # Extract order clause and remove it from where_clause
        order_field = m_order.group('field')
        dir_str = m_order.group('dir')
        if dir_str:
            order_dir = dir_str.upper()
        where_clause = where_clause[:m_order.start()].strip()

    # Step 3: Parse simple condition
    m_cond = _RE_SIMPLE_COND.fullmatch(where_clause)
    if not m_cond:
        raise ValueError("WHERE clause must be a simple condition (field op value)")

    cond_field = m_cond.group('field')
    cond_op_str = m_cond.group('op')
    cond_value_raw = m_cond.group('value')

    if cond_op_str not in _OPERATOR_MAP:
        raise ValueError(f"Unsupported operator '{cond_op_str}'")
    cond_value = _parse_value(cond_value_raw)
    op_func = _OPERATOR_MAP[cond_op_str]

    # Step 4: Validate fields
    all_keys = set(records[0].keys())
    if fields_str.strip() == '*':
        select_fields = list(all_keys)
    else:
        select_fields = [f.strip() for f in fields_str.split(',')]
        for f in select_fields:
            if f not in all_keys:
                raise ValueError(f"Field '{f}' does not exist in records")

    if cond_field not in all_keys:
        raise ValueError(f"Condition field '{cond_field}' does not exist")

    if order_field and order_field not in all_keys:
        raise ValueError(f"Order field '{order_field}' does not exist")

    # Step 5: Filter records
    filtered = [rec for rec in records if _evaluate_condition(rec, cond_field, op_func, cond_value)]

    # Step 6: Order if requested
    if order_field:
        reverse = (order_dir == 'DESC')
        try:
            filtered.sort(key=lambda r: r[order_field], reverse=reverse)
        except TypeError:
            raise ValueError(f"Cannot order by field '{order_field}' due to incomparable types")

    # Step 7: Project fields
    result = [{k: rec[k] for k in select_fields} for rec in filtered]
    return result
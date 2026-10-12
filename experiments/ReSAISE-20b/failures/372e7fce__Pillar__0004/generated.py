import re
import operator
from functools import reduce

# Mapping of supported operators to actual functions
_OP_MAP = {
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt
}

# Regular expressions for parsing the query components
_RE_SELECT = re.compile(r'\s*SELECT\s+(?P<cols>[\*\w,\s]+)', re.IGNORECASE)
_RE_FROM   = re.compile(r'\s+FROM\s+\w+', re.IGNORECASE)  # ignored
_RE_WHERE  = re.compile(r'\s+WHERE\s+(?P<cond>.+?)', re.IGNORECASE)
_RE_ORDER  = re.compile(r'\s+ORDER\s+BY\s+(?P<col>\w+)(?:\s+(?P<dir>ASC|DESC))?', re.IGNORECASE)

# Helper to parse a simple condition (no parentheses)
def _parse_condition(cond_str):
    # Split by AND
    parts = [p.strip() for p in cond_str.split('AND')]
    conditions = []
    for part in parts:
        # Find operator
        match = None
        for op_sym in sorted(_OP_MAP.keys(), key=len, reverse=True):
            if op_sym in part:
                match = re.split(r'\s*' + re.escape(op_sym) + r'\s*', part, maxsplit=1)
                op = _OP_MAP[op_sym]
                break
        if not match:
            raise ValueError(f"Unsupported condition: {part}")
        left, right = match
        # Resolve value (strip quotes if present)
        if right.startswith(("'", '"')) and right.endswith(("'", '"')):
            value = right[1:-1]
        else:
            # Try to interpret as number
            try:
                value = int(right)
            except ValueError:
                try:
                    value = float(right)
                except ValueError:
                    # treat as string without quotes
                    value = right.strip()
        conditions.append((left, op, value))
    return conditions

def _apply_conditions(record, conditions):
    # All ANDed
    for field, op_func, value in conditions:
        if field not in record:
            return False
        try:
            rec_val = record[field]
        except Exception:
            return False
        # Compare; try to coerce types if needed
        try:
            if isinstance(rec_val, (int, float)) and not isinstance(value, (int, float)):
                value = type(rec_val)(value)
        except Exception:
            pass
        if not op_func(rec_val, value):
            return False
    return True

def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a simple SQL-like query on an in-memory list of dictionaries.

    Parameters
    ----------
    dataset_list : list[dict]
        The data to query.
    sql_query : str
        SQL-like statement. Supports SELECT, WHERE (==, !=, >, <, >=, <= with AND),
        and ORDER BY. FROM clause is ignored.

    Returns
    -------
    list[dict]
        Query result set.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list of dictionaries.")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string.")

    # SELECT
    m = _RE_SELECT.search(sql_query)
    if not m:
        raise ValueError("Missing or malformed SELECT clause.")
    cols_raw = m.group('cols').strip()
    if cols_raw == '*':
        selected_cols = None  # all columns
    else:
        selected_cols = [c.strip() for c in cols_raw.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name in SELECT clause.")

    # WHERE
    where_cond = None
    m_where = _RE_WHERE.search(sql_query)
    if m_where:
        cond_str = m_where.group('cond').strip()
        where_cond = _parse_condition(cond_str)

    # ORDER BY
    order_col = None
    order_dir = 'ASC'
    m_order = _RE_ORDER.search(sql_query)
    if m_order:
        order_col = m_order.group('col')
        dir_str = m_order.group('dir')
        if dir_str:
            order_dir = dir_str.upper()

    # Filter records
    result = []
    for rec in dataset_list:
        if not isinstance(rec, dict):
            continue
        if where_cond and not _apply_conditions(rec, where_cond):
            continue
        # Project columns
        if selected_cols is None:
            proj = rec.copy()
        else:
            # If a column missing, set to None
            proj = {c: rec.get(c) for c in selected_cols}
        result.append(proj)

    # Order results
    if order_col:
        try:
            reverse = (order_dir == 'DESC')
            result.sort(key=lambda r: r.get(order_col), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Ordering failed: {e}")

    return result
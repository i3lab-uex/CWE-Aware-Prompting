import re
import operator
from functools import cmp_to_key
from typing import List, Dict, Any

# Mapping of string operators to actual functions
_OPS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Regular expression patterns for parsing the query
_SELECT_RE = re.compile(r'\s*SELECT\s+(?P<cols>[\w\*,\s]+)', re.IGNORECASE)
_WHERE_RE = re.compile(r'\s+WHERE\s+(?P<cond>.+)', re.IGNORECASE)
_ORDERBY_RE = re.compile(r'\s+ORDER\s+BY\s+(?P<col>\w+)\s*(?P<dir>ASC|DESC)?', re.IGNORECASE)

_COND_RE = re.compile(
    r'(?P<col>\w+)\s*(?P<op>=|==|!=|<>|<=?|>=?)\s*'
    r'(?P<val>(?:\'[^\']*\'|"[^"]*"|\d+(\.\d+)?))',
    re.IGNORECASE
)

def _parse_value(val: str) -> Any:
    """Convert a string value to int, float or strip quotes."""
    if val.startswith(("'", '"')) and val.endswith(("'", '"')):
        return val[1:-1]
    try:
        if '.' in val:
            return float(val)
        else:
            return int(val)
    except ValueError:
        raise ValueError(f"Unable to parse value: {val}")

def _evaluate_condition(row: Dict[str, Any], cond_str: str) -> bool:
    """Evaluate a simple condition on a row."""
    m = _COND_RE.fullmatch(cond_str.strip())
    if not m:
        raise ValueError(f"Invalid WHERE condition: {cond_str}")
    col, op_sym, val_raw = m.group('col'), m.group('op'), m.group('val')
    if col not in row:
        raise ValueError(f"Column {col!r} not found in data")
    op_func = _OPS[op_sym]
    val = _parse_value(val_raw)
    return op_func(row[col], val)

def execute_custom_query(data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT col1, col2, ... | *
        [WHERE condition]
        [ORDER BY column ASC|DESC]

    Only single simple conditions are supported in WHERE.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries")

    # 1. Parse SELECT
    m = _SELECT_RE.match(query)
    if not m:
        raise ValueError("Query must start with SELECT clause")
    cols_part = m.group('cols')
    selected_cols = [c.strip() for c in cols_part.split(',')]
    if len(selected_cols) == 1 and selected_cols[0] == '*':
        selected_cols = None  # means all columns
    else:
        for col in selected_cols:
            if not any(col in row for row in data):
                raise ValueError(f"Selected column {col!r} not found in data")

    # 2. Parse WHERE (optional)
    where_cond = None
    remainder = query[m.end():]
    m_where = _WHERE_RE.search(remainder)
    if m_where:
        where_cond = m_where.group('cond')
        remainder = remainder[m_where.end():]

    # 3. Parse ORDER BY (optional)
    order_col = None
    order_dir = 'ASC'
    m_order = _ORDERBY_RE.search(remainder)
    if m_order:
        order_col = m_order.group('col')
        dir_str = m_order.group('dir')
        if dir_str:
            order_dir = dir_str.upper()
        if not any(order_col in row for row in data):
            raise ValueError(f"ORDER BY column {order_col!r} not found in data")

    # 4. Filter rows
    result_rows = []
    for row in data:
        if where_cond is None or _evaluate_condition(row, where_cond):
            # Project columns
            if selected_cols is None:
                projected = dict(row)
            else:
                projected = {c: row.get(c) for c in selected_cols}
            result_rows.append(projected)

    # 5. Order rows
    if order_col:
        reverse = (order_dir == 'DESC')
        try:
            result_rows.sort(key=lambda r: r.get(order_col), reverse=reverse)
        except TypeError:
            # Mixed types; fallback to string comparison
            result_rows.sort(key=lambda r: str(r.get(order_col)), reverse=reverse)

    return result_rows
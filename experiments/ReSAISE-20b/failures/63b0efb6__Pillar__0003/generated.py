import re
import operator
from functools import reduce

# Mapping of supported comparison operators to functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expression patterns for parsing the SQL‑like command
_SELECT_RE = re.compile(r'\s*SELECT\s+(?P<cols>[\w\*,\s]+)\s+FROM\s+\S+', re.IGNORECASE)
_WHERE_RE = re.compile(r'\s*WHERE\s+(?P<cond>.+?)\s*(ORDER|$)', re.IGNORECASE)
_ORDER_BY_RE = re.compile(r'\s*ORDER\s+BY\s+(?P<order>[\w,.\s]+)', re.IGNORECASE)


def _parse_select(command: str):
    """Return a list of selected column names."""
    m = _SELECT_RE.search(command)
    if not m:
        raise ValueError("Malformed SELECT clause")
    cols = m.group('cols').strip()
    if cols == '*':
        return None  # select all columns
    return [c.strip() for c in cols.split(',') if c.strip()]


def _parse_where(command: str):
    """Return a lambda that evaluates the WHERE condition."""
    m = _WHERE_RE.search(command)
    if not m:
        return lambda rec: True  # no condition
    cond_str = m.group('cond').strip()

    # Very simple parser: column op value
    parts = re.split(r'\s+(=|!=|<>|>=|<=|>|<)\s+', cond_str, maxsplit=1)
    if len(parts) != 3:
        raise ValueError("Malformed WHERE clause")
    col, op_str, val_raw = parts
    if op_str not in _OP_MAP:
        raise ValueError(f"Unsupported operator '{op_str}'")
    op_func = _OP_MAP[op_str]

    # Determine the type of value (int, float, or string)
    if re.fullmatch(r'\d+', val_raw):
        val = int(val_raw)
    elif re.fullmatch(r'\d+\.\d*', val_raw):
        val = float(val_raw)
    elif re.fullmatch(r"'.*'", val_raw) or re.fullmatch(r'".*"', val_raw):
        val = val_raw[1:-1]
    else:
        # Assume it's a column name for equality comparison
        val = None

    def evaluator(rec):
        try:
            left = rec.get(col)
            right = val if val is not None else rec.get(val_raw)
            return op_func(left, right)
        except Exception:
            return False

    return evaluator


def _parse_order_by(command: str):
    """Return a list of (column, ascending) tuples."""
    m = _ORDER_BY_RE.search(command)
    if not m:
        return None
    order_str = m.group('order').strip()
    parts = [p.strip() for p in order_str.split(',')]
    orders = []
    for part in parts:
        if part.lower().endswith(' desc'):
            col = part[:-5].strip()
            asc = False
        elif part.lower().endswith(' asc'):
            col = part[:-4].strip()
            asc = True
        else:
            col = part
            asc = True
        orders.append((col, asc))
    return orders


def run_sql_query(records: list[dict], command: str) -> list[dict]:
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    records : list[dict]
        Input dataset.
    command : str
        SQL‑like statement (supports SELECT, WHERE, ORDER BY).

    Returns
    -------
    list[dict]
        Query result.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ValueError("Records must be a list of dictionaries")

    # SELECT
    cols = _parse_select(command)

    # WHERE
    where_func = _parse_where(command)

    # ORDER BY
    order_spec = _parse_order_by(command)

    # Apply WHERE filter
    filtered = list(filter(where_func, records))

    # Apply ORDER BY if specified
    if order_spec:
        def sort_key(rec):
            key = []
            for col, asc in order_spec:
                val = rec.get(col)
                # None values are placed at the end
                key.append((val is None, val if asc else _invert(val)))
            return tuple(key)

        def _invert(v):
            # Simple inversion for numeric and string types
            if isinstance(v, (int, float)):
                return -v
            if isinstance(v, str):
                # Reverse string for descending sort (not perfect but works)
                return ''.join(chr(255 - ord(c)) for c in v)
            return v

        filtered.sort(key=sort_key)

    # Project columns
    if cols is None:
        result = filtered
    else:
        result = [{c: rec.get(c) for c in cols} for rec in filtered]

    return result
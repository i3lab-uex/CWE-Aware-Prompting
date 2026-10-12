import re
import operator
from functools import reduce

# Supported binary operators for WHERE clauses
OPS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

def _parse_select(query):
    """Parse the SELECT part of the query."""
    m = re.search(r'\bSELECT\b\s+(.*?)\s+\bFROM\b', query, re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("Missing or malformed SELECT clause.")
    fields = [f.strip() for f in m.group(1).split(',')]
    if fields == ['*']:
        return None  # means all fields
    return fields

def _parse_where(query):
    """Parse the WHERE part of the query."""
    m = re.search(r'\bWHERE\b\s+(.*?)(\bORDER\b|\Z)', query, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    condition_str = m.group(1).strip()
    # Very simple parsing: support only single binary operation per condition
    for op_sym in sorted(OPS, key=len, reverse=True):
        if op_sym in condition_str:
            left, right = [p.strip() for p in condition_str.split(op_sym, 1)]
            # try to interpret right as a literal number or string
            if re.match(r"^'(.*)'$", right):
                right_val = re.match(r"^'(.*)'$", right).group(1)
            else:
                try:
                    right_val = int(right)
                except ValueError:
                    try:
                        right_val = float(right)
                    except ValueError:
                        right_val = right  # treat as string if not numeric
            return (left, OPS[op_sym], right_val)
    raise ValueError("Unsupported WHERE condition.")

def _parse_order_by(query):
    """Parse the ORDER BY part of the query."""
    m = re.search(r'\bORDER\s+BY\b\s+(.*)', query, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    order_part = m.group(1).strip()
    # allow optional ASC/DESC
    parts = order_part.split()
    field = parts[0]
    direction = parts[1].upper() if len(parts) > 1 else 'ASC'
    if direction not in ('ASC', 'DESC'):
        raise ValueError("ORDER BY direction must be ASC or DESC.")
    return (field, direction == 'ASC')

def _apply_where(record, condition):
    """Return True if record satisfies the condition."""
    field, op_func, value = condition
    if field not in record:
        return False
    try:
        return op_func(record[field], value)
    except Exception:
        return False

def execute_query_cmd(dataset_list, sql_query):
    """
    Execute a very small subset of SQL on an in‑memory list of dictionaries.

    Supported syntax:
        SELECT <columns> FROM <table>
        [WHERE <field> <op> <value>]
        [ORDER BY <field> [ASC|DESC]]

    Parameters
    ----------
    dataset_list : list[dict]
        The data to query.
    sql_query : str
        The SQL‑like statement.

    Returns
    -------
    list[dict]
        Result rows.
    """
    if not isinstance(dataset_list, list) or any(not isinstance(r, dict) for r in dataset_list):
        raise ValueError("dataset_list must be a list of dictionaries.")

    # Normalise whitespace and case for parsing
    query = re.sub(r'\s+', ' ', sql_query.strip())

    # Parse SELECT
    select_fields = _parse_select(query)

    # Parse WHERE
    where_cond = _parse_where(query)

    # Parse ORDER BY
    order_by = _parse_order_by(query)

    # Filter records
    if where_cond:
        filtered = [r for r in dataset_list if _apply_where(r, where_cond)]
    else:
        filtered = list(dataset_list)

    # Order records
    if order_by:
        field, ascending = order_by
        try:
            filtered.sort(key=lambda r: r.get(field), reverse=not ascending)
        except TypeError:
            raise ValueError(f"Cannot order by field '{field}' due to incomparable types.")

    # Project fields
    if select_fields is not None:
        result = [{k: r.get(k) for k in select_fields} for r in filtered]
    else:
        result = [dict(r) for r in filtered]

    return result
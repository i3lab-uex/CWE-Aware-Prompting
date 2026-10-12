import re
import operator
from functools import reduce

# Mapping of supported comparison operators
OPS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(r"^\s*SELECT\s+(?P<fields>[\w\*,\s]+)\s+WHERE\s+(?P<cond>.+?)\s*ORDER\s+BY\s+(?P<order>\w+)\s*(?:ASC|DESC)?\s*$",
                       re.IGNORECASE | re.DOTALL)
WHERE_RE = re.compile(r"(?P<field>\w+)\s*(?P<op>=|!=|>|<|>=|<=)\s*'?(?P<value>[^'\s]+)'?", re.IGNORECASE)
ORDER_DIR_RE = re.compile(r"(ASC|DESC)", re.IGNORECASE)

def _parse_select(query: str):
    """Parse SELECT query into components."""
    m = SELECT_RE.match(query)
    if not m:
        raise ValueError("Query must be of form: SELECT ... WHERE ... ORDER BY ...")
    fields = [f.strip() for f in m.group("fields").split(",")]
    cond_str = m.group("cond")
    order_field = m.group("order").strip()
    return fields, cond_str, order_field

def _parse_where(cond_str: str):
    """Parse WHERE clause into a list of (field, op, value) tuples."""
    conds = []
    for m in WHERE_RE.finditer(cond_str):
        field, op, value = m.group("field", "op", "value")
        conds.append((field, op, value))
    if not conds:
        raise ValueError("No valid conditions found in WHERE clause")
    return conds

def _apply_where(row: dict, conds):
    """Return True if row satisfies all conditions."""
    for field, op, value in conds:
        # Convert numeric values when possible
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                val = value
        if field not in row:
            return False
        # Attempt to convert the row's value to same type as val
        try:
            row_val = int(row[field])
        except (ValueError, TypeError):
            try:
                row_val = float(row[field])
            except (ValueError, TypeError):
                row_val = row[field]
        if not OPS[op](row_val, val):
            return False
    return True

def execute_custom_query(data: list[dict], query: str) -> list[dict]:
    """
    Execute a simplified SQL-like query on a list of dictionaries.

    Parameters
    ----------
    data : list[dict]
        Dataset to query.
    query : str
        SQL-like query string. Example:
            "SELECT name, age WHERE age > '30' ORDER BY name ASC"

    Returns
    -------
    list[dict]
        List of dictionaries that match the query.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(data, list) or any(not isinstance(r, dict) for r in data):
        raise ValueError("Data must be a list of dictionaries")

    fields, cond_str, order_field = _parse_select(query)
    conds = _parse_where(cond_str)

    # Filter rows
    filtered = [row for row in data if _apply_where(row, conds)]

    # Order rows
    reverse = ORDER_DIR_RE.search(query) and ORDER_DIR_RE.search(query).group(1).upper() == "DESC"
    try:
        filtered.sort(key=lambda r: r.get(order_field), reverse=reverse)
    except TypeError as e:
        raise ValueError(f"Cannot order by field '{order_field}': {e}")

    # Project fields
    if fields == ['*']:
        result = filtered
    else:
        result = [{k: r.get(k) for k in fields} for r in filtered]

    return result
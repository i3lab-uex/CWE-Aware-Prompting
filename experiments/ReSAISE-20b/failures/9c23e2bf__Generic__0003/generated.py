import re
import operator
from functools import reduce

# Supported binary operators for WHERE clause
OPS = {
    "==": operator.eq,
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
}

# Regular expression to parse a very simple SQL‑like query
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<columns>[\*\w,\s]+)\s*
    (?:WHERE\s+(?P<where>[^ORDER]*?)\s*)?
    (?:ORDER\s+BY\s+(?P<orderby>[\w]+)(?:\s+(?P<orderdir>ASC|DESC))?)?
    \s*;?\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to parse a simple condition
_COND_RE = re.compile(
    r"""
    ^\s*(?P<field>\w+)\s*
    (?P<op>==|!=|<>|<=|>=|<|>|=)\s*
    (?P<value>.+?)\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_value(val: str):
    """Try to interpret a value as int, float or keep it as string."""
    val = val.strip()
    if (val.startswith("'") and val.endswith("'")) or (
        val.startswith('"') and val.endswith('"')
    ):
        return val[1:-1]
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        # Treat as string without quotes
        return val


def _build_where_func(where_clause: str):
    """Return a function that evaluates the WHERE clause for a record."""
    match = _COND_RE.match(where_clause)
    if not match:
        raise ValueError(f"Unsupported WHERE clause: {where_clause}")

    field = match.group("field")
    op_str = match.group("op")
    value_raw = match.group("value")

    if op_str not in OPS:
        raise ValueError(f"Unsupported operator {op_str} in WHERE clause")

    op_func = OPS[op_str]
    value = _parse_value(value_raw)

    def predicate(record):
        try:
            return op_func(record.get(field), value)
        except Exception:
            return False

    return predicate


def run_custom_query(dataset, query):
    """
    Execute a very small subset of SQL-like queries on an in‑memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        List of records, each record is a dictionary.
    query : str
        SQL‑like statement. Supports:
            SELECT <columns>
            WHERE <field> <op> <value>
            ORDER BY <column> [ASC|DESC]
        The query may end with a semicolon.

    Returns
    -------
    list[dict]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query syntax is invalid or unsupported.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")

    match = _QUERY_RE.match(query)
    if not match:
        raise ValueError("Invalid query format")

    columns_str = match.group("columns").strip()
    where_clause = match.group("where")
    orderby_col = match.group("orderby")
    order_dir = match.group("orderdir") or "ASC"

    # SELECT *
    if columns_str == "*":
        selected_columns = None  # keep all fields
    else:
        selected_columns = [c.strip() for c in columns_str.split(",") if c.strip()]
        if not selected_columns:
            raise ValueError("No columns specified in SELECT clause")

    # Apply WHERE
    if where_clause:
        predicate = _build_where_func(where_clause)
        filtered = list(filter(predicate, dataset))
    else:
        filtered = list(dataset)

    # Apply ORDER BY
    if orderby_col:
        reverse = order_dir.upper() == "DESC"
        try:
            filtered.sort(key=lambda r: r.get(orderby_col), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot order by column '{orderby_col}': {exc}")

    # Apply SELECT projection
    if selected_columns is not None:
        result = [{k: rec.get(k) for k in selected_columns} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
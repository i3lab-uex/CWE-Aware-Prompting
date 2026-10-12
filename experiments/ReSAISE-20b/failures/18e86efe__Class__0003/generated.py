import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual functions
_OP_MAP = {
    "=": operator.eq,
    "==": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le
}

# Regular expression to parse a very small subset of SQL
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<select>[\w,\s*]+)\s+
    (?:FROM\s+\w+\s+)?                     # ignore FROM clause
    (?:WHERE\s+(?P<where>[^;]+?)\s+)?      # optional WHERE
    (?:ORDER\s+BY\s+(?P<order>\w+)\s*)?    # optional ORDER BY
    ;?\s*$                                  # optional trailing semicolon
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to split a simple condition into left, operator, right
_COND_RE = re.compile(
    r"""
    (?P<field>\w+)\s*
    (?P<op>==|!=|<>|>=|<=|>|<)\s*
    (?P<value>.+)
    """,
    re.VERBOSE,
)

def _parse_value(val: str) -> Any:
    """Parse a literal value (int, float, or string)."""
    val = val.strip()
    # Quoted strings
    if (val.startswith("'") and val.endswith("'")) or (
        val.startswith('"') and val.endswith('"')
    ):
        return val[1:-1]
    # Numeric values
    try:
        if "." in val:
            return float(val)
        else:
            return int(val)
    except ValueError:
        # Treat as string if parsing fails
        return val

def _build_where_func(condition: str):
    """Return a function that evaluates the condition for a record."""
    match = _COND_RE.fullmatch(condition.strip())
    if not match:
        raise ValueError(f"Invalid WHERE condition: {condition!r}")
    field, op_str, value_raw = match.group("field", "op", "value")
    op_func = _OP_MAP.get(op_str)
    if not op_func:
        raise ValueError(f"Unsupported operator: {op_str!r}")
    value = _parse_value(value_raw)

    def predicate(record):
        try:
            return op_func(record.get(field), value)
        except Exception as exc:
            raise ValueError(f"Error evaluating condition on record {record}: {exc}") from exc

    return predicate

def run_user_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL on an in‑memory dataset.

    Supported syntax:
        SELECT <fields> [FROM <table>] [WHERE <condition>] [ORDER BY <field>];

    * Fields can be `*` or a comma‑separated list of keys.
    * Condition supports a single comparison (no AND/OR).
    * ORDER BY sorts ascending by the specified field.

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    sql_query : str
        The SQL‑like query string.

    Returns
    -------
    List[Dict[str, Any]]
        The resulting records after applying SELECT/WHERE/ORDER BY.

    Raises
    ------
    ValueError
        If the query string is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    match = _QUERY_RE.fullmatch(sql_query.strip())
    if not match:
        raise ValueError("Query syntax is invalid")

    select_part = match.group("select").strip()
    where_part = match.group("where")
    order_by_field = match.group("order")

    # Determine which fields to return
    if select_part == "*":
        selected_fields = None  # keep all keys
    else:
        selected_fields = [f.strip() for f in select_part.split(",") if f.strip()]
        if not selected_fields:
            raise ValueError("SELECT clause must specify at least one field")

    # Build WHERE predicate if present
    where_pred = None
    if where_part:
        where_pred = _build_where_func(where_part)

    # Filter records
    try:
        filtered = (
            record for record in dataset if (where_pred(record) if where_pred else True)
        )
    except Exception as exc:
        raise ValueError(f"Error filtering dataset: {exc}") from exc

    # Select fields
    if selected_fields is not None:
        def select(record):
            return {k: record.get(k) for k in selected_fields}
    else:
        def select(record):
            return dict(record)

    try:
        result = [select(rec) for rec in filtered]
    except Exception as exc:
        raise ValueError(f"Error selecting fields: {exc}") from exc

    # Order by if specified
    if order_by_field:
        try:
            result.sort(key=lambda r: r.get(order_by_field))
        except Exception as exc:
            raise ValueError(f"Error ordering by {order_by_field}: {exc}") from exc

    return result
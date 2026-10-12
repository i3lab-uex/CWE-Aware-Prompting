import re
import operator
from functools import partial
from typing import List, Dict, Any

# Mapping of supported operators to their corresponding functions.
_OPERATOR_MAP = {
    "=": operator.eq,
    "==": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

# Regular expression to parse a very small subset of SQL.
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<fields>[\w\s,]+?)          # SELECT <fields>
    (?:\s+WHERE\s+(?P<where>[^ORDER]+?))?      # optional WHERE clause
    (?:\s+ORDER\s+BY\s+(?P<orderby>[\w]+)      # ORDER BY <field>
        (?:\s+(?P<orderdir>ASC|DESC))?)?      # optional ASC/DESC
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to parse a simple condition: <field> <operator> <value>
_COND_RE = re.compile(
    r"""
    ^\s*(?P<field>\w+)\s*
    (?P<op>==|!=|<>|>=|<=|>|<)\s*
    (?P<value>.+?)\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)

def _parse_value(val: str) -> Any:
    """Attempt to convert a string value into int, float or keep as stripped string."""
    val = val.strip()
    # Remove surrounding quotes if present
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Try integer
    try:
        return int(val)
    except ValueError:
        pass
    # Try float
    try:
        return float(val)
    except ValueError:
        pass
    # Return as string
    return val

def _evaluate_condition(record: Dict[str, Any], cond_str: str) -> bool:
    """Evaluate a simple condition against a single record."""
    m = _COND_RE.match(cond_str)
    if not m:
        raise ValueError(f"Unsupported WHERE condition: {cond_str!r}")
    field = m.group("field")
    op_sym = m.group("op")
    val_str = m.group("value")

    if field not in record:
        raise ValueError(f"Field {field!r} does not exist in records")

    op_func = _OPERATOR_MAP.get(op_sym)
    if op_func is None:
        raise ValueError(f"Unsupported operator {op_sym!r}")

    record_value = record[field]
    compare_value = _parse_value(val_str)

    try:
        return op_func(record_value, compare_value)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate condition: {exc}") from exc

def submit_user_query(records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The dataset to query.
    sql_statement : str
        Query string. Supported syntax:
            SELECT <fields> [WHERE <field> <op> <value>] [ORDER BY <field> [ASC|DESC]]

    Returns
    -------
    List[Dict[str, Any]]
        Query result.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not all(isinstance(rec, dict) for rec in records):
        raise ValueError("all items in records must be dictionaries")

    m = _QUERY_RE.match(sql_statement)
    if not m:
        raise ValueError("Query format is invalid")

    fields_str = m.group("fields")
    where_clause = m.group("where")
    orderby_field = m.group("orderby")
    orderdir = m.group("orderdir")

    # Parse fields
    fields = [f.strip() for f in fields_str.split(",") if f.strip()]
    if not fields:
        raise ValueError("No fields specified in SELECT clause")

    # Validate that requested fields exist
    for field in fields:
        if not any(field in rec for rec in records):
            raise ValueError(f"Field {field!r} does not exist in any record")

    # Filter records if WHERE clause present
    filtered = records
    if where_clause:
        filtered = [rec for rec in records if _evaluate_condition(rec, where_clause)]

    # Order results
    if orderby_field:
        if not any(orderby_field in rec for rec in records):
            raise ValueError(f"ORDER BY field {orderby_field!r} does not exist")
        reverse = orderdir and orderdir.upper() == "DESC"
        try:
            filtered.sort(key=lambda r: r.get(orderby_field, None), reverse=reverse)
        except TypeError as exc:
            raise ValueError(f"Cannot sort by field {orderby_field!r}: {exc}") from exc

    # Project selected fields
    result = [{field: rec.get(field) for field in fields} for rec in filtered]
    return result
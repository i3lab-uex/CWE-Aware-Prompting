import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Map string operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge
}

# Regular expression to parse the query
QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<fields>[\w\*,\s]+)\s+          # SELECT clause
    (?:FROM\s+\w+\s+)?                              # Optional FROM clause (ignored)
    (?P<where>WHERE\s+(?P<cond>.+?)\s+)?            # Optional WHERE clause
    (?P<order>ORDER\s+BY\s+(?P<orderby>.+))?\s*$   # Optional ORDER BY clause
    """,
    re.IGNORECASE | re.VERBOSE
)

# Regular expression to parse a simple condition (field op value)
COND_RE = re.compile(
    r"""
    (?P<field>\w+)\s*
    (?P<op>=|!=|<=|>=|<|>)\s*
    (?P<value>.+)
    """,
    re.VERBOSE
)

def _parse_value(val: str) -> Any:
    """Convert string literal to int, float or stripped string."""
    val = val.strip()
    # Remove surrounding quotes if present
    if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Try numeric conversion
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        pass
    # Fallback: raw string
    return val

def _evaluate_condition(record: Dict[str, Any], cond: str) -> bool:
    """Evaluate a simple condition against a record."""
    m = COND_RE.match(cond)
    if not m:
        raise ValueError(f"Unsupported condition syntax: {cond!r}")
    field, op_str, val_str = m.group('field', 'op', 'value')
    if field not in record:
        raise ValueError(f"Field {field!r} not found in record")
    op_func = OPERATORS[op_str]
    field_value = record[field]
    comp_value = _parse_value(val_str)
    try:
        return op_func(field_value, comp_value)
    except TypeError as exc:
        raise ValueError(f"Type mismatch in condition {cond!r}") from exc

def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset_list : list[dict]
        The dataset to query.
    sql_query : str
        SQL-like statement (SELECT, optional WHERE, optional ORDER BY).

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the query syntax is invalid or cannot be processed.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    match = QUERY_RE.match(sql_query)
    if not match:
        raise ValueError("Query syntax is invalid")

    fields_part = match.group('fields')
    where_cond = match.group('cond')
    orderby_part = match.group('orderby')

    # Parse fields
    if fields_part.strip() == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in fields_part.split(',')]
        if not all(selected_fields):
            raise ValueError("Field names cannot be empty")

    # Filter records
    if where_cond:
        try:
            filtered = [rec for rec in dataset_list if _evaluate_condition(rec, where_cond)]
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc
    else:
        filtered = list(dataset_list)

    # Order by
    if orderby_part:
        order_fields = [f.strip() for f in orderby_part.split(',')]
        # Support only simple ascending ordering
        def sort_key(rec):
            return tuple(rec.get(f, None) for f in order_fields)
        try:
            filtered.sort(key=sort_key)
        except TypeError as exc:
            raise ValueError(f"Cannot order by specified fields: {exc}") from exc

    # Project fields
    if selected_fields is None:
        result = [dict(rec) for rec in filtered]
    else:
        result = []
        for rec in filtered:
            projected = {}
            for f in selected_fields:
                if f not in rec:
                    raise ValueError(f"Field {f!r} not found in record")
                projected[f] = rec[f]
            result.append(projected)

    return result
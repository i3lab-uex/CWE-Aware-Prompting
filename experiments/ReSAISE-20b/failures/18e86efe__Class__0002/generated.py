import re
import operator
from functools import cmp_to_key
from typing import List, Dict

# Mapping of supported comparison operators to functions from operator module.
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge
}

# Regular expression to parse a very simple SQL‑like query.
_QUERY_RE = re.compile(
    r"""
    ^\s*SELECT\s+(?P<select>[\*\w,\s]+)          # SELECT clause
    (?:\s+WHERE\s+(?P<where>[^;]+?))?           # optional WHERE clause
    (?:\s+ORDER\s+BY\s+(?P<order>\w+))?         # optional ORDER BY clause
    \s*;?\s*$                                   # optional trailing semicolon
    """,
    re.IGNORECASE | re.VERBOSE
)

# Regular expression to parse a simple condition in the WHERE clause.
_CONDITION_RE = re.compile(
    r"""
    ^\s*(?P<col>\w+)\s*
    (?P<op>=|!=|<=|>=|<|>)\s*
    (?P<val>.+?)\s*$
    """,
    re.VERBOSE
)

def _parse_value(val: str):
    """Parse a string literal into an int, float or stripped string."""
    val = val.strip()
    # Remove surrounding quotes if present
    if (val.startswith("'") and val.endswith("'")) or (
        val.startswith('"') and val.endswith('"')
    ):
        return val[1:-1]
    # Try numeric conversion
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        # Treat as plain string
        return val

def _build_where_func(where_clause: str):
    """Return a function that evaluates the WHERE condition for a record."""
    match = _CONDITION_RE.match(where_clause)
    if not match:
        raise ValueError(f"Invalid WHERE clause: {where_clause!r}")

    col = match.group('col')
    op_str = match.group('op')
    val_raw = match.group('val')

    if op_str not in _OPERATOR_MAP:
        raise ValueError(f"Unsupported operator {op_str!r}")

    op_func = _OPERATOR_MAP[op_str]
    val = _parse_value(val_raw)

    def predicate(record: Dict):
        try:
            record_val = record.get(col)
            return op_func(record_val, val)
        except Exception:
            # If the column is missing or comparison fails
            return False

    return predicate

def run_user_query(dataset: List[Dict], sql_query: str) -> List[Dict]:
    """
    Execute a simple SQL‑like query on an in‑memory dataset.

    Supported syntax:
        SELECT <columns> [WHERE <column> <op> <value>] [ORDER BY <column>];
    Columns can be a comma separated list or '*'.
    Operators: =, !=, <, >, <=, >=.
    ORDER BY is ascending only.

    Parameters
    ----------
    dataset : list of dict
        The data to query.
    sql_query : str
        Query string.

    Returns
    -------
    list of dict
        The filtered, projected and sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries.")
    if not isinstance(sql_query, str):
        raise ValueError("Query must be a string.")

    # Parse the query
    m = _QUERY_RE.match(sql_query)
    if not m:
        raise ValueError("Query format is invalid.")

    select_part = m.group('select')
    where_part = m.group('where')
    order_part = m.group('order')

    # Determine selected columns
    select_columns = [c.strip() for c in select_part.split(',')] if select_part != '*' else None

    # Build WHERE predicate
    where_func = _build_where_func(where_part) if where_part else lambda _: True

    # Apply filtering
    try:
        filtered = list(filter(where_func, dataset))
    except Exception as e:
        raise ValueError(f"Error during filtering: {e}") from e

    # Apply ordering
    if order_part:
        try:
            filtered.sort(key=lambda rec: rec.get(order_part))
        except Exception as e:
            raise ValueError(f"Error during ordering: {e}") from e

    # Apply projection
    if select_columns is not None:
        try:
            projected = [{k: rec.get(k) for k in select_columns} for rec in filtered]
        except Exception as e:
            raise ValueError(f"Error during projection: {e}") from e
    else:
        projected = filtered

    return projected
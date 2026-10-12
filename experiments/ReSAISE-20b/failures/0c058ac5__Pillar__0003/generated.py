import re
import operator as op
from functools import partial
from typing import List, Dict

# Mapping of supported operators in the WHERE clause to actual Python functions
_OPERATOR_MAP = {
    '=': op.eq,
    '!=': op.ne,
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le
}

# Regular expression patterns for parsing the SQL-like statement.
_QUERY_RE = re.compile(
    r'''
    ^\s*SELECT\s+(?P<select>[\w*,\s]+)\s+      # SELECT clause
    (?:FROM\s+\w+\s*)?                        # Optional FROM clause
    (?:WHERE\s+(?P<where>[^;]+?)\s*)?         # Optional WHERE clause
    (?:ORDER\s+BY\s+(?P<order>[\w,\s]+))?     # Optional ORDER BY clause
    \s*;?\s*$                                  # Optional trailing semicolon and whitespace
    ''',
    re.IGNORECASE | re.VERBOSE
)

# Regular expression for a simple comparison expression in WHERE clause.
_CONDITION_RE = re.compile(
    r'''
    (?P<field>\w+)\s*
    (?P<op>!=|>=|<=|=|>|<)\s*
    (?P<value>'[^']*'|"[^"]*"|\d+(\.\d*)?)
    ''',
    re.VERBOSE
)

def _parse_value(token: str):
    """Parse a value token from the WHERE clause."""
    if token.startswith(("'", '"')) and token.endswith(("'", '"')):
        return token[1:-1]
    try:
        if '.' in token:
            return float(token)
        return int(token)
    except ValueError as exc:
        raise ValueError(f"Invalid value in WHERE clause: {token}") from exc

def _build_condition(field, op_str, value):
    """Return a function that evaluates the condition for a record."""
    if op_str not in _OPERATOR_MAP:
        raise ValueError(f"Unsupported operator: {op_str}")
    compare_func = _OPERATOR_MAP[op_str]
    return lambda rec: compare_func(rec.get(field), value)

def _parse_where(where_clause: str):
    """Parse the WHERE clause into a list of condition functions."""
    conditions = []
    for match in _CONDITION_RE.finditer(where_clause):
        field, op_str, value_token = match.group('field', 'op', 'value')
        value = _parse_value(value_token)
        conditions.append(_build_condition(field, op_str, value))
    return conditions

def submit_user_query(records: List[Dict], sql_statement: str) -> List[Dict]:
    """
    Execute a simple SQL-like query on a list of dictionary records.

    Parameters
    ----------
    records : List[Dict]
        Dataset to query.
    sql_statement : str
        SQL-like statement containing SELECT, optional WHERE and ORDER BY.

    Returns
    -------
    List[Dict]
        Query result set.

    Raises
    ------
    ValueError
        If the statement is malformed or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    match = _QUERY_RE.match(sql_statement)
    if not match:
        raise ValueError("Invalid SQL-like statement format")

    select_part = match.group('select')
    where_part = match.group('where')
    order_part = match.group('order')

    # Determine fields to return
    if select_part.strip() == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in select_part.split(',')]
        # Validate field names against the first record (if any)
        if records:
            for f in selected_fields:
                if f not in records[0]:
                    raise ValueError(f"Unknown field in SELECT clause: {f}")

    # Apply WHERE filtering
    filtered = records
    if where_part:
        conditions = _parse_where(where_part)
        # Ensure all fields referenced in WHERE exist
        for cond in conditions:
            if not isinstance(cond, partial):
                pass  # no action needed
        filtered = [rec for rec in records if all(cond(rec) for cond in conditions)]

    # Apply ORDER BY sorting
    if order_part:
        order_fields = [f.strip() for f in order_part.split(',')]
        # Validate fields
        for f in order_fields:
            if records and f not in records[0]:
                raise ValueError(f"Unknown field in ORDER BY clause: {f}")
        # Sort by multiple fields (stable sort)
        for f in reversed(order_fields):
            filtered.sort(key=lambda rec: rec.get(f))

    # Project selected fields
    if selected_fields is not None:
        result = [{k: rec.get(k) for k in selected_fields} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
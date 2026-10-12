import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,          # alternative not equal
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le
}

# Regular expressions for parsing the query
_SELECT_RE = re.compile(r'^\s*SELECT\s+(?P<fields>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
_WHERE_RE = re.compile(
    r'WHERE\s+(?P<field>\w+)\s*(?P<op>=|!=|<>|>|>=|<|<=)\s*'
    r'(?P<value>(?:\'[^\']*\'|"[^"]*"|[^\s]+))',
    re.IGNORECASE
)
_ORDERBY_RE = re.compile(
    r'ORDER\s+BY\s+(?P<field>\w+)(?:\s+(?P<dir>ASC|DESC))?',
    re.IGNORECASE
)

def _parse_value(val: str) -> Any:
    """Parse a value from the WHERE clause, converting to int/float if possible."""
    # Strip quotes if present
    if (val.startswith("'") and val.endswith("'")) or \
       (val.startswith('"') and val.endswith('"')):
        return val[1:-1]
    # Try numeric conversion
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        # Return as string if conversion fails
        return val

def _apply_where(records: List[Dict[str, Any]],
                 field: str,
                 op_func,
                 value: Any) -> List[Dict[str, Any]]:
    """Filter records according to a single WHERE condition."""
    filtered = []
    for rec in records:
        if field not in rec:
            continue
        try:
            if op_func(rec[field], value):
                filtered.append(rec)
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc
    return filtered

def _apply_orderby(records: List[Dict[str, Any]],
                   field: str,
                   ascending: bool = True) -> List[Dict[str, Any]]:
    """Sort records by a field."""
    try:
        return sorted(records, key=lambda r: r.get(field), reverse=not ascending)
    except Exception as exc:
        raise ValueError(f"Error during ORDER BY: {exc}") from exc

def _select_fields(records: List[Dict[str, Any]],
                   fields: List[str]) -> List[Dict[str, Any]]:
    """Project selected fields."""
    if '*' in fields:
        return records
    result = []
    for rec in records:
        new_rec = {f: rec.get(f) for f in fields}
        result.append(new_rec)
    return result

def execute_user_query(records: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL‑like query on an in‑memory list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        Dataset to query.
    user_query : str
        Query string.  Supported syntax:

            SELECT <fields> FROM <table>
            [WHERE <field> <op> <value>]
            [ORDER BY <field> [ASC|DESC]]

    Returns
    -------
    List[Dict[str, Any]]
        Result set after applying SELECT/WHERE/ORDER BY.

    Raises
    ------
    ValueError
        If the query syntax is invalid or evaluation fails.
    """
    if not isinstance(user_query, str):
        raise ValueError("Query must be a string")

    # ---------- SELECT ----------
    m = _SELECT_RE.match(user_query)
    if not m:
        raise ValueError("Invalid SELECT syntax")
    fields_part = m.group('fields')
    fields = [f.strip() for f in fields_part.split(',')]
    if not fields:
        raise ValueError("No fields specified in SELECT")

    # ---------- WHERE ----------
    where_clause = None
    m_where = _WHERE_RE.search(user_query)
    if m_where:
        field = m_where.group('field')
        op_str = m_where.group('op')
        raw_value = m_where.group('value')
        value = _parse_value(raw_value)
        op_func = _OP_MAP.get(op_str.upper())
        if not op_func:
            raise ValueError(f"Unsupported operator in WHERE clause: {op_str}")
        where_clause = (field, op_func, value)

    # ---------- ORDER BY ----------
    order_by_clause = None
    m_order = _ORDERBY_RE.search(user_query)
    if m_order:
        order_field = m_order.group('field')
        dir_str = m_order.group('dir')
        ascending = True if not dir_str or dir_str.upper() == 'ASC' else False
        order_by_clause = (order_field, ascending)

    # ---------- Execution ----------
    try:
        result = records
        if where_clause:
            result = _apply_where(result, *where_clause)
        if order_by_clause:
            result = _apply_orderby(result, *order_by_clause)
        result = _select_fields(result, fields)
    except Exception as exc:
        raise ValueError(f"Query execution failed: {exc}") from exc

    return result
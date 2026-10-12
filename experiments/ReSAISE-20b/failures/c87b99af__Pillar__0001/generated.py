import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported operators for WHERE clause
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regex patterns for parsing the query components
_SELECT_RE = re.compile(r'^SELECT\s+(?P<select>[\*\w,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
_WHERE_RE = re.compile(r'WHERE\s+(?P<where>.+)', re.IGNORECASE)
_ORDER_BY_RE = re.compile(r'ORDER\s+BY\s+(?P<orderby>[\w]+)\s*(?P<direction>\bASC\b|\bDESC\b)?', re.IGNORECASE)

# Pattern to validate a simple condition: column op value
_CONDITION_RE = re.compile(r'^\s*(?P<col>\w+)\s*(?P<op>=|!=|>|<|>=|<=)\s*(?P<val>.+?)\s*$')

def _parse_select(select_clause: str) -> List[str]:
    """Parse SELECT clause into a list of column names or ['*']."""
    cols = [c.strip() for c in select_clause.split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return ['*']
    if not all(cols):
        raise ValueError("Empty column name in SELECT clause")
    return cols

def _parse_where(where_clause: str) -> List[Dict[str, Any]]:
    """Parse WHERE clause into a list of condition dictionaries."""
    # For simplicity we only support a single condition
    m = _CONDITION_RE.match(where_clause)
    if not m:
        raise ValueError("Invalid WHERE condition syntax")
    col, op_str, val_raw = m.group('col'), m.group('op'), m.group('val')
    # Attempt to interpret the value as int, float or keep string
    try:
        val = int(val_raw)
    except ValueError:
        try:
            val = float(val_raw)
        except ValueError:
            # strip surrounding quotes if present
            val = val_raw.strip("'\"")
    return [{'col': col, 'op': _OP_MAP[op_str], 'val': val}]

def _apply_where(records: List[Dict[str, Any]], conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter records according to the list of conditions."""
    def record_satisfies(rec: Dict[str, Any]) -> bool:
        for cond in conditions:
            if cond['col'] not in rec or not cond['op'](rec[cond['col']], cond['val']):
                return False
        return True
    return [rec for rec in records if record_satisfies(rec)]

def _apply_order_by(records: List[Dict[str, Any]], orderby_clause: str) -> List[Dict[str, Any]]:
    """Sort records based on ORDER BY clause."""
    m = _ORDER_BY_RE.match(orderby_clause)
    if not m:
        raise ValueError("Invalid ORDER BY syntax")
    col = m.group('orderby')
    direction = m.group('direction')
    reverse = direction and direction.upper() == 'DESC'
    try:
        return sorted(records, key=lambda r: r.get(col), reverse=reverse)
    except TypeError:
        raise ValueError(f"Cannot order by column '{col}' due to incomparable values")

def execute_user_query(records: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL‑like query on an in‑memory list of dictionaries.

    Supported syntax:
        SELECT <columns> FROM <table>
        [WHERE <column> <op> <value>]
        [ORDER BY <column> [ASC|DESC]]

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The dataset to query.
    user_query : str
        SQL‑like query string.

    Returns
    -------
    List[Dict[str, Any]]
        The result of the query.

    Raises
    ------
    ValueError
        If the query syntax is invalid or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Normalize query
    q = user_query.strip()
    if not q.lower().startswith('select'):
        raise ValueError("Query must start with SELECT")

    # Extract SELECT clause
    select_match = _SELECT_RE.search(q)
    if not select_match:
        raise ValueError("Invalid SELECT syntax")
    selected_cols = _parse_select(select_match.group('select'))

    # Extract WHERE clause if present
    where_clause = None
    where_match = _WHERE_RE.search(q)
    if where_match:
        where_clause = where_match.group('where')

    # Extract ORDER BY clause if present
    orderby_clause = None
    orderby_match = _ORDER_BY_RE.search(q)
    if orderby_match:
        # rebuild the full ORDER BY part
        orderby_clause = q[orderby_match.start():orderby_match.end()]

    # Apply WHERE filter
    filtered = records
    if where_clause:
        conditions = _parse_where(where_clause)
        filtered = _apply_where(filtered, conditions)

    # Apply ORDER BY
    if orderby_clause:
        filtered = _apply_order_by(filtered, orderby_clause)

    # Apply SELECT projection
    if selected_cols == ['*']:
        result = filtered
    else:
        # Ensure requested columns exist in all records; missing keys are omitted
        result = [{k: rec[k] for k in selected_cols if k in rec} for rec in filtered]

    return result
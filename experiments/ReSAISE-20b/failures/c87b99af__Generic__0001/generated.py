import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Supported operators for WHERE clauses
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regular expressions for parsing the query
_SELECT_RE = re.compile(r'^SELECT\s+(?P<cols>[\w\*,\s]+)\s+FROM\s+\w+', re.IGNORECASE)
_WHERE_RE = re.compile(r'WHERE\s+(?P<cond>.+?)\s*(ORDER BY|$)', re.IGNORECASE)
_ORDER_BY_RE = re.compile(r'ORDER\s+BY\s+(?P<col>\w+)(?:\s+(?P<dir>ASC|DESC))?', re.IGNORECASE)
# Simple condition parser: column op value
_COND_RE = re.compile(r'(?P<col>\w+)\s*(?P<op>=|!=|<>|>|<|>=|<=)\s*(?P<val>.+)', re.IGNORECASE)

def _parse_select(query: str) -> List[str]:
    m = _SELECT_RE.search(query)
    if not m:
        raise ValueError("Malformed SELECT clause")
    cols = [c.strip() for c in m.group('cols').split(',')]
    return cols

def _parse_where(query: str) -> List[Dict[str, Any]]:
    m = _WHERE_RE.search(query)
    if not m:
        return []  # no WHERE
    cond_str = m.group('cond')
    # Support multiple conditions combined with AND
    parts = [p.strip() for p in re.split(r'\s+AND\s+', cond_str, flags=re.IGNORECASE)]
    conditions = []
    for part in parts:
        cm = _COND_RE.fullmatch(part)
        if not cm:
            raise ValueError(f"Malformed condition: {part}")
        col = cm.group('col')
        op = _OP_MAP[cm.group('op')]
        val_raw = cm.group('val').strip()
        # Try to interpret as int or float, otherwise strip quotes
        if (val_raw.startswith("'") and val_raw.endswith("'")) or (
            val_raw.startswith('"') and val_raw.endswith('"')
        ):
            val = val_raw[1:-1]
        else:
            try:
                if '.' in val_raw:
                    val = float(val_raw)
                else:
                    val = int(val_raw)
            except ValueError:
                # treat as string
                val = val_raw
        conditions.append({'col': col, 'op': op, 'val': val})
    return conditions

def _parse_order_by(query: str) -> Dict[str, Any]:
    m = _ORDER_BY_RE.search(query)
    if not m:
        return {}
    col = m.group('col')
    dir_ = m.group('dir') or 'ASC'
    return {'col': col, 'dir': dir_.upper()}

def _apply_conditions(record: Dict[str, Any], conditions: List[Dict[str, Any]]) -> bool:
    return all(cond['op'](record.get(cond['col']), cond['val']) for cond in conditions)

def execute_user_query(records: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        Dataset to query.
    user_query : str
        Query string containing SELECT, optional WHERE and ORDER BY clauses.

    Returns
    -------
    List[Dict[str, Any]]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Normalize query
    q = user_query.strip()

    # Parse clauses
    try:
        select_cols = _parse_select(q)
        where_conditions = _parse_where(q)
        order_by = _parse_order_by(q)
    except Exception as exc:
        raise ValueError(f"Failed to parse query: {exc}") from exc

    # Validate selected columns
    if select_cols == ['*']:
        final_select = None  # means all columns
    else:
        for col in select_cols:
            if not any(col in rec for rec in records):
                raise ValueError(f"Unknown column in SELECT: {col}")

    # Filter records
    try:
        filtered = [rec for rec in records if _apply_conditions(rec, where_conditions)]
    except Exception as exc:
        raise ValueError(f"Error applying WHERE conditions: {exc}") from exc

    # Order records
    if order_by:
        col = order_by['col']
        reverse = order_by['dir'] == 'DESC'
        try:
            filtered.sort(key=lambda r: r.get(col), reverse=reverse)
        except Exception as exc:
            raise ValueError(f"Error ordering by {col}: {exc}") from exc

    # Project columns
    result = []
    for rec in filtered:
        if final_select is None:
            result.append(rec.copy())
        else:
            projected = {c: rec.get(c) for c in select_cols}
            result.append(projected)

    return result
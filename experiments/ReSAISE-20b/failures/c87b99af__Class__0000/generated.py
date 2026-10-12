import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported comparison operators to their python functions.
_OP_MAP = {
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>':  operator.gt,
    '<':  operator.lt
}

# Regular expressions for parsing the query.
_RE_SELECT = re.compile(r'^\s*SELECT\s+(?P<cols>[\w\*,\s]+)\s+WHERE\s+(?P<where>.+?)\s*(ORDER\s+BY\s+(?P<orderby>[\w,\s]+))?\s*$', re.IGNORECASE)
_RE_WHERE_COND = re.compile(r'(?P<left>\w+)\s*(?P<op>==|!=|>=|<=|>|<)\s*(?P<right>\S+)', re.IGNORECASE)
_RE_ORDERBY = re.compile(r'\s*(?P<col>\w+)\s*(?P<dir>ASC|DESC)?\s*', re.IGNORECASE)


def _parse_where_clause(where_str: str):
    """
    Parse the WHERE clause into a list of (column, operator, value) tuples.
    Supports only simple AND conjunctions.
    """
    conditions = []
    for part in re.split(r'\s+AND\s+', where_str, flags=re.IGNORECASE):
        m = _RE_WHERE_COND.match(part.strip())
        if not m:
            raise ValueError(f"Invalid WHERE condition: '{part}'")
        col, op, val = m.group('left'), m.group('op'), m.group('right')
        # Strip quotes if present
        if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            # Try to interpret as number
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass  # keep as string
        conditions.append((col, _OP_MAP[op], val))
    return conditions


def _evaluate_conditions(record: Dict[str, Any], conditions):
    """
    Evaluate all conditions against a single record.
    """
    for col, op_func, val in conditions:
        if col not in record:
            return False
        try:
            if not op_func(record[col], val):
                return False
        except Exception:
            return False
    return True


def _parse_orderby(orderby_str: str):
    """
    Parse ORDER BY clause into a list of (column, reverse) tuples.
    """
    order_list = []
    for part in re.split(r',\s*', orderby_str):
        m = _RE_ORDERBY.match(part)
        if not m:
            raise ValueError(f"Invalid ORDER BY clause: '{part}'")
        col = m.group('col')
        dir_ = m.group('dir') or 'ASC'
        reverse = dir_.upper() == 'DESC'
        order_list.append((col, reverse))
    return order_list


def execute_user_query(records: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionary records.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        The dataset to query.
    user_query : str
        The SQL-like query string.

    Returns
    -------
    List[Dict[str, Any]]
        The resulting list of records after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query format is invalid or execution fails.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries")
    if not isinstance(user_query, str):
        raise ValueError("user_query must be a string")

    m = _RE_SELECT.match(user_query)
    if not m:
        raise ValueError("Query must match SELECT <columns> WHERE <conditions> [ORDER BY <cols>]")

    # Parse selected columns
    cols_str = m.group('cols').strip()
    if cols_str == '*':
        selected_cols = None  # indicates all columns
    else:
        selected_cols = [c.strip() for c in cols_str.split(',')]
        if not all(selected_cols):
            raise ValueError("Invalid column names in SELECT clause")

    # Parse WHERE conditions
    where_str = m.group('where')
    try:
        conditions = _parse_where_clause(where_str)
    except ValueError as e:
        raise ValueError(f"WHERE clause error: {e}")

    # Parse ORDER BY if present
    orderby_str = m.group('orderby')
    order_list = []
    if orderby_str:
        try:
            order_list = _parse_orderby(orderby_str)
        except ValueError as e:
            raise ValueError(f"ORDER BY clause error: {e}")

    # Filter records
    filtered = [rec for rec in records if _evaluate_conditions(rec, conditions)]

    # Order results
    if order_list:
        def sort_key(rec):
            return tuple(
                rec.get(col, None) for col, _ in order_list
            )
        # Sort with stable sort applying each level in reverse order for DESC
        for col, reverse in reversed(order_list):
            filtered.sort(key=lambda r: r.get(col, None), reverse=reverse)

    # Project selected columns
    if selected_cols is not None:
        result = [{k: v for k, v in rec.items() if k in selected_cols} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
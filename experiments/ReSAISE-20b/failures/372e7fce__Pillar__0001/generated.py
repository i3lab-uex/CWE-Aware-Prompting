import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of supported comparison operators
_COMP_OPS = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def _parse_select_part(sql: str):
    """Parse the SELECT part of the query."""
    m = re.match(r'\s*SELECT\s+(?P<cols>.+?)\s+FROM\b', sql, re.IGNORECASE)
    if not m:
        raise ValueError("Malformed SELECT clause")
    cols = [c.strip() for c in m.group('cols').split(',')]
    return cols

def _parse_where_part(sql: str):
    """Parse the WHERE part of the query if present."""
    m = re.search(r'\bWHERE\b\s+(?P<cond>.+?)\s*(ORDER BY|$)', sql, re.IGNORECASE)
    if not m:
        return None
    cond_str = m.group('cond').strip()
    # Very simple condition: column op value
    for op_str in sorted(_COMP_OPS, key=len, reverse=True):
        parts = cond_str.split(op_str)
        if len(parts) == 2:
            col, val_raw = parts[0].strip(), parts[1].strip()
            # Try to interpret value as int or float, else keep string
            try:
                val = int(val_raw)
            except ValueError:
                try:
                    val = float(val_raw)
                except ValueError:
                    # strip surrounding quotes if present
                    val = re.sub(r"^['\"]|['\"]$", "", val_raw)
            return lambda rec, col=col, op=_COMP_OPS[op_str], val=val: op(rec.get(col), val)
    raise ValueError("Unsupported WHERE condition")

def _parse_order_by_part(sql: str):
    """Parse ORDER BY part of the query if present."""
    m = re.search(r'\bORDER\s+BY\b\s+(?P<col>\w+)\s*(?P<dir>ASC|DESC)?', sql, re.IGNORECASE)
    if not m:
        return None
    col = m.group('col')
    direction = m.group('dir')
    reverse = (direction and direction.upper() == 'DESC')
    return col, reverse

def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL on an in-memory list of dictionaries.
    Supported syntax:
        SELECT <columns> FROM <any>
        Optional: WHERE <column> <op> <value>
        Optional: ORDER BY <column> [ASC|DESC]
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list")
    if not isinstance(sql_query, str):
        raise ValueError("sql_query must be a string")

    # Normalize whitespace and case
    sql = re.sub(r'\s+', ' ', sql_query.strip())

    # SELECT clause
    selected_cols = _parse_select_part(sql)
    if len(selected_cols) == 1 and selected_cols[0] == '*':
        selected_cols = None  # means all columns

    # WHERE clause
    where_func = _parse_where_part(sql)

    # ORDER BY clause
    order_info = _parse_order_by_part(sql)
    if order_info:
        order_col, reverse_flag = order_info
    else:
        order_col, reverse_flag = None, False

    # Filter records
    try:
        filtered = (rec for rec in dataset_list if where_func(rec) if where_func else True)
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Sort if needed
    try:
        result = list(filtered)
        if order_col:
            result.sort(key=lambda r: r.get(order_col), reverse=reverse_flag)
    except Exception as e:
        raise ValueError(f"Error during ORDER BY: {e}")

    # Project columns
    if selected_cols:
        try:
            projected = [{col: rec.get(col) for col in selected_cols} for rec in result]
        except Exception as e:
            raise ValueError(f"Error projecting columns: {e}")
    else:
        projected = result

    return projected
import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Map string operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regex patterns for parsing
SELECT_PATTERN = re.compile(r'\s*select\s+(?P<fields>[\*\w,\s]+)\s+from\s+\w+', re.IGNORECASE)
WHERE_PATTERN = re.compile(r'\s*where\s+(?P<cond>.+)', re.IGNORECASE)
ORDER_PATTERN = re.compile(r'\s*order\s+by\s+(?P<field>\w+)(?:\s+(?P<dir>asc|desc))?', re.IGNORECASE)

def _parse_where(cond: str):
    """Parse a simple WHERE clause of the form `field op value`."""
    # Split into tokens: field, operator, value
    for op_sym in sorted(OPERATORS.keys(), key=len, reverse=True):
        if op_sym in cond:
            field, value = map(str.strip, cond.split(op_sym, 1))
            return field, OPERATORS[op_sym], _parse_value(value)
    raise ValueError(f"Unsupported WHERE clause: {cond}")

def _parse_value(val_str: str):
    """Attempt to convert a string value to int/float or strip quotes."""
    val_str = val_str.strip()
    if (val_str.startswith('"') and val_str.endswith('"')) or \
       (val_str.startswith("'") and val_str.endswith("'")):
        return val_str[1:-1]
    try:
        if '.' in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        # Treat as string if cannot convert
        return val_str

def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL on an in‑memory dataset.

    Parameters
    ----------
    dataset_list : list[dict]
        List of records, each a dictionary.
    sql_query : str
        SQL-like statement. Supported syntax:
          SELECT <fields> FROM <table>
          [WHERE <field> <op> <value>]
          [ORDER BY <field> [ASC|DESC]]

    Returns
    -------
    list[dict]
        The result set after applying SELECT, WHERE and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset_list, list):
        raise ValueError("dataset_list must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset_list):
        raise ValueError("All items in dataset_list must be dictionaries")

    # 1. SELECT
    m = SELECT_PATTERN.match(sql_query)
    if not m:
        raise ValueError("SELECT clause missing or malformed")
    fields_str = m.group('fields').strip()
    if fields_str == '*':
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in fields_str.split(',')]
        # Validate field names
        if dataset_list:
            all_keys = set(dataset_list[0].keys())
            for f in selected_fields:
                if f not in all_keys:
                    raise ValueError(f"Field '{f}' does not exist in dataset")

    # 2. WHERE
    where_func = None
    rest_query = sql_query[m.end():]
    m_where = WHERE_PATTERN.search(rest_query)
    if m_where:
        cond_str = m_where.group('cond')
        try:
            field, op_func, value = _parse_where(cond_str)
        except Exception as e:
            raise ValueError(f"Error parsing WHERE clause: {e}")
        where_func = lambda rec, f=field, op=op_func, v=value: op(rec.get(f), v)

    # 3. ORDER BY
    order_func = None
    m_order = ORDER_PATTERN.search(rest_query)
    if m_order:
        order_field = m_order.group('field')
        direction = (m_order.group('dir') or 'asc').lower()
        reverse = direction == 'desc'
        if dataset_list and order_field not in dataset_list[0]:
            raise ValueError(f"Order field '{order_field}' does not exist in dataset")
        order_func = lambda rec, f=order_field: rec.get(f)

    # Apply WHERE filter
    if where_func:
        filtered = [rec for rec in dataset_list if where_func(rec)]
    else:
        filtered = list(dataset_list)

    # Apply ORDER BY
    if order_func:
        try:
            filtered.sort(key=order_func, reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by field '{order_field}': {e}")

    # Apply SELECT projection
    if selected_fields is not None:
        result = [{k: rec[k] for k in selected_fields} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
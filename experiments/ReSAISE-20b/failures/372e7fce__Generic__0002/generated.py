import re
import operator
from functools import partial
from typing import List, Dict, Any

def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL‑like query on an in‑memory dataset.

    Supported syntax:
        SELECT <field1>,<field2> | *
        [WHERE <field> <op> <value>]
        [ORDER BY <field> ASC|DESC]

    Operators in WHERE: =, !=, >, >=, <, <=
    Values may be numeric or a quoted string ('text' or "text").

    Parameters
    ----------
    dataset_list : List[Dict[str, Any]]
        The data to query.
    sql_query : str
        The SQL‑like statement.

    Returns
    -------
    List[Dict[str, Any]]
        Query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset_list, list) or any(not isinstance(r, dict) for r in dataset_list):
        raise ValueError("dataset_list must be a list of dictionaries")

    # Normalize whitespace and upper‑case keywords for parsing
    query = re.sub(r'\s+', ' ', sql_query.strip())
    pattern = re.compile(
        r'^SELECT\s+(?P<fields>[\*\w,\s]+)'
        r'(?:\s+WHERE\s+(?P<where>.+?))?'
        r'(?:\s+ORDER\s+BY\s+(?P<order_field>\w+)\s*(?P<order_dir>ASC|DESC)?)?$',
        re.IGNORECASE
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Invalid query format")

    # Parse SELECT fields
    raw_fields = match.group('fields').strip()
    if raw_fields == '*':
        selected_fields = None  # means all fields
    else:
        selected_fields = [f.strip() for f in raw_fields.split(',')]
        if not all(selected_fields):
            raise ValueError("Empty field name in SELECT clause")

    # Parse WHERE clause
    where_clause = match.group('where')
    filter_func = None
    if where_clause:
        # Only support a single condition (no AND/OR)
        cond_match = re.match(
            r'^(?P<field>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<value>.+)$',
            where_clause.strip()
        )
        if not cond_match:
            raise ValueError("Invalid WHERE clause")
        field = cond_match.group('field')
        op_str = cond_match.group('op')
        value_raw = cond_match.group('value').strip()

        # Strip quotes if present
        if (value_raw.startswith("'") and value_raw.endswith("'")) or \
           (value_raw.startswith('"') and value_raw.endswith('"')):
            value = value_raw[1:-1]
        else:
            # Try to interpret as int or float
            try:
                if '.' in value_raw:
                    value = float(value_raw)
                else:
                    value = int(value_raw)
            except ValueError:
                # Treat as string if not numeric
                value = value_raw

        op_map = {
            '=': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge,
            '<': operator.lt,
            '<=': operator.le
        }
        op_func = op_map[op_str]

        def filter_func(record, f=field, v=value, op=op_func):
            if f not in record:
                raise ValueError(f"Field '{f}' not found in records")
            return op(record[f], v)

    # Apply filtering
    result = dataset_list
    if filter_func:
        try:
            result = [rec for rec in result if filter_func(rec)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Apply ORDER BY
    order_field = match.group('order_field')
    if order_field:
        reverse = (match.group('order_dir') or '').upper() == 'DESC'
        try:
            result = sorted(result, key=lambda r: r.get(order_field), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by field '{order_field}': {e}")

    # Project selected fields
    if selected_fields is not None:
        projected = []
        for rec in result:
            proj = {}
            for f in selected_fields:
                if f not in rec:
                    raise ValueError(f"Field '{f}' not found in records")
                proj[f] = rec[f]
            projected.append(proj)
        result = projected

    return result
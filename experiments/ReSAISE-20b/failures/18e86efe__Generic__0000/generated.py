import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Supported binary operators mapping to python functions
OPS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}

def _parse_where_clause(where_str: str):
    """
    Very small parser that splits a simple expression of the form
    <field> <op> <value>. Only one condition is supported.
    """
    pattern = r'^\s*(\w+)\s*([=!<>]{1,2})\s*(.+?)\s*$'
    m = re.match(pattern, where_str)
    if not m:
        raise ValueError(f"Invalid WHERE clause: {where_str!r}")

    field, op_sym, value_raw = m.groups()
    if op_sym not in OPS:
        raise ValueError(f"Unsupported operator {op_sym!r}")

    # Try to convert value to int or float if possible, else strip quotes
    try:
        value = int(value_raw)
    except ValueError:
        try:
            value = float(value_raw)
        except ValueError:
            # Strip surrounding quotes if present
            value = re.sub(r"^['\"]|['\"]$", "", value_raw)

    return lambda record: OPS[op_sym](record.get(field), value)


def _parse_order_by_clause(order_str: str):
    """
    Parse ORDER BY clause. Supports one field optionally followed by ASC|DESC.
    Returns a tuple (field_name, reverse_bool)
    """
    parts = order_str.strip().split()
    if not parts:
        raise ValueError("ORDER BY clause is empty")
    field = parts[0]
    reverse = False
    if len(parts) > 1:
        dir_ = parts[1].upper()
        if dir_ == 'DESC':
            reverse = True
        elif dir_ != 'ASC':
            raise ValueError(f"Unsupported ORDER BY direction: {parts[1]}")
    return field, reverse


def run_user_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a very small subset of SQL against an in‑memory list of dicts.
    Supported syntax:
        SELECT <field1>, <field2>, ... [WHERE <condition>] [ORDER BY <field> [ASC|DESC]]
    The SELECT clause is mandatory. WHERE and ORDER BY are optional.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("dataset must be a list of dictionaries")

    # Basic regex to capture clauses
    pattern = re.compile(
        r'''
        ^\s*SELECT\s+(?P<select>[^W]*?)          # SELECT fields
        (?:\s+WHERE\s+(?P<where>[^O]*?))?       # optional WHERE
        (?:\s+ORDER\s+BY\s+(?P<order>.*))?      # optional ORDER BY
        \s*$                                    # end of string
        ''',
        re.IGNORECASE | re.VERBOSE
    )
    m = pattern.match(sql_query)
    if not m:
        raise ValueError("Query format is invalid")

    select_fields = [f.strip() for f in m.group('select').split(',') if f.strip()]
    if not select_fields:
        raise ValueError("SELECT clause must specify at least one field")

    # Validate that requested fields exist in dataset (if not empty)
    if dataset:
        for f in select_fields:
            if f not in dataset[0]:
                raise ValueError(f"Field {f!r} does not exist in dataset")

    # WHERE
    where_func = None
    if m.group('where'):
        where_func = _parse_where_clause(m.group('where'))

    # ORDER BY
    order_field, reverse_flag = None, False
    if m.group('order'):
        order_field, reverse_flag = _parse_order_by_clause(m.group('order'))
        if dataset and order_field not in dataset[0]:
            raise ValueError(f"ORDER BY field {order_field!r} not found in dataset")

    # Apply filtering
    result = dataset
    if where_func:
        try:
            result = list(filter(where_func, result))
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}") from e

    # Apply ordering
    if order_field:
        try:
            result.sort(key=lambda r: r.get(order_field), reverse=reverse_flag)
        except Exception as e:
            raise ValueError(f"Error during ORDER BY: {e}") from e

    # Project selected fields
    final = [{k: rec.get(k) for k in select_fields} for rec in result]

    return final
#!/usr/bin/env python3
"""
A minimal, safe SQL‑like query executor for in‑memory data.
Supports:
    SELECT <fields>
    FROM <dummy>   # ignored, only one dataset is supplied
    WHERE <condition>
    ORDER BY <field> [ASC|DESC]
"""

import re
import operator
from functools import reduce
from typing import Any, Callable, Dict, List

# --------------------------------------------------------------------------- #
#  Helpers for parsing and evaluating expressions
# --------------------------------------------------------------------------- #

# Supported comparison operators mapped to functions
COMPARE_OPS: Dict[str, Callable[[Any, Any], bool]] = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}

LOGICAL_OPS: Dict[str, Callable[[bool, bool], bool]] = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

# Regex patterns
SELECT_RE = re.compile(r'\s*SELECT\s+(?P<select>[\w\*,\s]+)\s+FROM\s+\S+', re.IGNORECASE)
WHERE_RE = re.compile(r'\s*WHERE\s+(?P<where>.+)', re.IGNORECASE)
ORDER_RE = re.compile(r'\s*ORDER\s+BY\s+(?P<order>\w+)(?:\s+(?P<dir>ASC|DESC))?', re.IGNORECASE)

# Tokenize a simple condition string
CONDITION_TOKEN_RE = re.compile(r'''
    (?P<field>\w+)
    \s*
    (?P<op>=|!=|<=|>=|<|>)
    \s*
    (?P<value>
        '(?:\\'|[^'])*' |   # quoted string
        \d+(?:\.\d+)?       # number
    )
''', re.VERBOSE)

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def run_sql_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simplified SQL query on an in‑memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        A SQL‑like string containing SELECT, WHERE, ORDER BY clauses.

    Returns
    -------
    list[dict]
        The query result as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query cannot be parsed or executed.
    """
    if not isinstance(dataset, list):
        raise ValueError('dataset must be a list of dictionaries')
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError('each record must be a dictionary')

    # 1. Parse SELECT clause
    select_match = SELECT_RE.search(sql_query)
    if not select_match:
        raise ValueError('Missing or malformed SELECT clause')
    raw_select = select_match.group('select').strip()
    if raw_select == '*':
        selected_fields = None  # means all fields
    else:
        selected_fields = [f.strip() for f in raw_select.split(',')]
        if not all(selected_fields):
            raise ValueError('Empty field name in SELECT clause')

    # 2. Parse WHERE clause (optional)
    where_func: Callable[[Dict[str, Any]], bool] | None = None
    where_match = WHERE_RE.search(sql_query)
    if where_match:
        condition_str = where_match.group('where').strip()
        where_func = _build_where_function(condition_str, dataset)

    # 3. Parse ORDER BY clause (optional)
    order_by_field: str | None = None
    reverse_order: bool = False
    order_match = ORDER_RE.search(sql_query)
    if order_match:
        order_by_field = order_match.group('order')
        dir_token = order_match.group('dir')
        reverse_order = (dir_token or '').upper() == 'DESC'

    # 4. Filter records
    try:
        if where_func is None:
            filtered = dataset
        else:
            filtered = [rec for rec in dataset if where_func(rec)]
    except Exception as exc:  # pragma: no cover
        raise ValueError(f'Error evaluating WHERE clause: {exc}') from exc

    # 5. Order records
    if order_by_field:
        try:
            filtered.sort(key=lambda r: _safe_value(r.get(order_by_field)), reverse=reverse_order)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f'Error ordering by {order_by_field}: {exc}') from exc

    # 6. Project fields
    if selected_fields is None:
        result = [dict(rec) for rec in filtered]
    else:
        result = [{k: rec.get(k) for k in selected_fields} for rec in filtered]

    return result


# --------------------------------------------------------------------------- #
#  Internal helpers
# --------------------------------------------------------------------------- #

def _build_where_function(cond_str: str, dataset: List[Dict[str, Any]]) -> Callable[[Dict[str, Any]], bool]:
    """
    Build a function that evaluates the WHERE condition for a record.
    Supports simple expressions combined with AND/OR (no parentheses).
    """
    tokens = []
    pos = 0
    length = len(cond_str)

    while pos < length:
        # Skip whitespace
        if cond_str[pos].isspace():
            pos += 1
            continue

        # Logical operator?
        if cond_str[pos:pos+3].upper() in LOGICAL_OPS:
            op = cond_str[pos:pos+3].upper()
            if op in LOGICAL_OPS:
                tokens.append(op)
                pos += 3
                continue

        # Field comparison
        m = CONDITION_TOKEN_RE.match(cond_str, pos)
        if not m:
            raise ValueError(f'Invalid condition near: {cond_str[pos:]}')
        field = m.group('field')
        op_token = m.group('op')
        raw_value = m.group('value')

        # Validate field exists in dataset
        if not any(field in rec for rec in dataset):
            raise ValueError(f'Field "{field}" does not exist in the dataset')

        # Parse value
        if raw_value.startswith("'"):
            val = _unescape_string(raw_value[1:-1])
        else:
            if '.' in raw_value:
                val = float(raw_value)
            else:
                val = int(raw_value)

        tokens.append((field, op_token, val))
        pos = m.end()

    # Build evaluation function
    def evaluator(record: Dict[str, Any]) -> bool:
        stack = []
        for token in tokens:
            if isinstance(token, str) and token in LOGICAL_OPS:
                # logical operator
                b = stack.pop()
                a = stack.pop()
                stack.append(LOGICAL_OPS[token](a, b))
            else:
                # comparison
                field, op_token, val = token
                rec_val = record.get(field)
                comp_func = COMPARE_OPS[op_token]
                stack.append(comp_func(rec_val, val))
        if len(stack) != 1:
            raise ValueError('Malformed WHERE clause')
        return bool(stack[0])

    return evaluator


def _unescape_string(s: str) -> str:
    """Handle escaped single quotes within a quoted string."""
    return s.replace("\\'", "'")


def _safe_value(v: Any) -> Any:
    """
    Convert values to a type that is safe for sorting.
    Non‑comparable types are converted to strings as a last resort.
    """
    try:
        return v
    except Exception:  # pragma: no cover
        return str(v)

# --------------------------------------------------------------------------- #
#  Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     data = [
#         {"id": 1, "name": "Alice", "age": 30},
#         {"id": 2, "name": "Bob",   "age": 25},
#         {"id": 3, "name": "Carol", "age": 27}
#     ]
#     query = """
#         SELECT id, name
#         FROM data
#         WHERE age >= 26 AND name != 'Bob'
#         ORDER BY id DESC
#     """
#     print(run_sql_query(data, query))
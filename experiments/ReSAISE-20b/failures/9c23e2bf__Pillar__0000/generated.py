import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual Python operator functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}

# Regular expressions for parsing the query
SELECT_RE = re.compile(
    r"^\s*SELECT\s+(?P<fields>[\w\*,\s]+)\s+FROM\s+\w+", re.IGNORECASE)
WHERE_RE = re.compile(
    r"\s+WHERE\s+(?P<condition>.+)", re.IGNORECASE)
ORDER_BY_RE = re.compile(
    r"\s+ORDER\s+BY\s+(?P<field>\w+)\s*(?P<direction>ASC|DESC)?", re.IGNORECASE)
COND_RE = re.compile(
    r"(?P<left>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<right>.+)")

def _parse_fields(fields_str: str) -> List[str]:
    fields = [f.strip() for f in fields_str.split(',')]
    if len(fields) == 1 and fields[0] == '*':
        return ['*']
    for f in fields:
        if not re.match(r'^\w+$', f):
            raise ValueError(f"Invalid field name: {f}")
    return fields

def _parse_condition(cond_str: str):
    match = COND_RE.fullmatch(cond_str.strip())
    if not match:
        raise ValueError(f"Invalid WHERE condition: {cond_str}")
    left = match.group('left')
    op_sym = match.group('op')
    right_raw = match.group('right').strip()
    # Try to interpret the right side as a number or keep string
    try:
        right = int(right_raw)
    except ValueError:
        try:
            right = float(right_raw)
        except ValueError:
            # strip quotes if present
            right = re.sub(r"^['\"]|['\"]$", "", right_raw)
    return left, OPERATORS[op_sym], right

def _apply_where(dataset: List[Dict[str, Any]], condition):
    left, op_func, right = condition
    result = []
    for row in dataset:
        if left not in row:
            raise ValueError(f"Field '{left}' not found in dataset")
        if op_func(row[left], right):
            result.append(row)
    return result

def _apply_order_by(dataset: List[Dict[str, Any]], field: str, direction: str):
    if not dataset:
        return []
    if field not in dataset[0]:
        raise ValueError(f"Field '{field}' not found for ORDER BY")
    reverse = direction.upper() == 'DESC'
    try:
        return sorted(dataset, key=lambda r: r[field], reverse=reverse)
    except TypeError as exc:
        raise ValueError(f"Cannot order by field '{field}': {exc}") from exc

def _apply_select(dataset: List[Dict[str, Any]], fields: List[str]):
    if fields == ['*']:
        return dataset
    result = []
    for row in dataset:
        new_row = {}
        for f in fields:
            if f not in row:
                raise ValueError(f"Field '{f}' not found for SELECT")
            new_row[f] = row[f]
        result.append(new_row)
    return result

def run_custom_query(dataset: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a limited SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query.
    query : str
        SQL-like string containing SELECT, optional WHERE and ORDER BY.

    Returns
    -------
    List[Dict[str, Any]]
        The resulting records after applying the query.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    # Parse SELECT clause
    select_match = SELECT_RE.search(query)
    if not select_match:
        raise ValueError("SELECT clause missing or malformed")
    fields = _parse_fields(select_match.group('fields'))

    # Parse optional WHERE clause
    where_match = WHERE_RE.search(query)
    if where_match:
        condition = _parse_condition(where_match.group('condition'))
        dataset = _apply_where(dataset, condition)

    # Parse optional ORDER BY clause
    order_match = ORDER_BY_RE.search(query)
    if order_match:
        field = order_match.group('field')
        direction = order_match.group('direction') or 'ASC'
        dataset = _apply_order_by(dataset, field, direction)

    # Apply SELECT projection
    result = _apply_select(dataset, fields)
    return result
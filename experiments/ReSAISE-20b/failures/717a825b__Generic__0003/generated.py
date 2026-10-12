import re
import operator
from functools import reduce

# Mapping of string operators to actual functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Supported logical operators
_LOGICAL_MAP = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_condition(cond_str):
    """
    Parse a simple condition string into a function that takes a row dict
    and returns True/False.
    Supports:
        - binary comparisons (field op value)
        - logical AND / OR chaining
    """
    # Tokenize by spaces, keep quoted strings together
    tokens = re.findall(r'(?:"[^"]*"|\'[^\']*\'|\S+)', cond_str)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Convert tokens to a list of evaluatable parts
    eval_parts = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        upper_token = token.upper()
        if upper_token in _LOGICAL_MAP:
            eval_parts.append(upper_token)
            i += 1
        else:
            # Expect pattern: field operator value
            if i + 2 >= len(tokens):
                raise ValueError(f"Incomplete condition near '{token}'")
            field = token
            op_token = tokens[i + 1]
            value_raw = tokens[i + 2]

            if op_token not in _OP_MAP:
                raise ValueError(f"Unsupported operator '{op_token}'")

            # Strip quotes if present
            if (value_raw.startswith('"') and value_raw.endswith('"')) or \
               (value_raw.startswith("'") and value_raw.endswith("'")):
                value = value_raw[1:-1]
            else:
                # Try to interpret as number
                try:
                    if '.' in value_raw:
                        value = float(value_raw)
                    else:
                        value = int(value_raw)
                except ValueError:
                    value = value_raw  # leave as string

            op_func = _OP_MAP[op_token]
            eval_parts.append((field, op_func, value))
            i += 3

    # Build a lambda that evaluates the condition
    def cond(row):
        result = None
        current_logic = None
        for part in eval_parts:
            if isinstance(part, tuple):
                field, op_func, value = part
                # Fetch field value from row; treat missing as None
                row_val = row.get(field, None)
                part_res = op_func(row_val, value)
            else:  # logical operator
                current_logic = _LOGICAL_MAP[part]
                continue

            if result is None:
                result = part_res
            else:
                # apply the previous logical operator
                result = current_logic(result, part_res)
        return bool(result)

    return cond

def _parse_order_by(order_str):
    """
    Parse ORDER BY clause into a key function and reverse flag.
    Example: "age DESC" -> (lambda r: r.get('age'), True)
    """
    parts = order_str.strip().split()
    if not parts:
        raise ValueError("Empty ORDER BY clause")
    field = parts[0]
    reverse = False
    if len(parts) > 1:
        direction = parts[1].upper()
        if direction == 'DESC':
            reverse = True
        elif direction != 'ASC':
            raise ValueError(f"Unsupported ORDER BY direction '{direction}'")
    return field, reverse

def execute_custom_query(data, query):
    """
    Execute a simple SQL‑like query on a list of dictionaries.

    Supported syntax:
        SELECT field1,field2,... FROM <ignored>
            [WHERE condition]
            [ORDER BY field ASC|DESC]

    Parameters
    ----------
    data : list[dict]
        The dataset to query.
    query : str
        The SQL‑like query string.

    Returns
    -------
    list[dict]
        List of result rows with only the selected fields.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(data, list):
        raise ValueError("data must be a list of dictionaries")
    if not all(isinstance(row, dict) for row in data):
        raise ValueError("All items in data must be dictionaries")

    # Basic regex to capture SELECT, WHERE, ORDER BY
    pattern = re.compile(
        r"""
        ^\s*SELECT\s+(?P<select>[\w*,\s]+)\s+
        (?:FROM\s+\S+\s+)?                 # FROM clause ignored
        (?P<where>WHERE\s+[^;]+?)?         # optional WHERE
        (?:\s+(?P<order>ORDER\s+BY\s+[^;]+))?  # optional ORDER BY
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE,
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Query does not match supported syntax")

    # Parse selected fields
    select_part = match.group('select')
    fields = [f.strip() for f in select_part.split(',') if f.strip()]
    if not fields:
        raise ValueError("No fields specified in SELECT clause")

    # Filter data
    result = data[:]
    where_part = match.group('where')
    if where_part:
        cond_str = where_part[len('WHERE'):].strip()
        condition_func = _parse_condition(cond_str)
        result = list(filter(condition_func, result))

    # Order data
    order_part = match.group('order')
    if order_part:
        order_str = order_part[len('ORDER BY'):].strip()
        field, reverse = _parse_order_by(order_str)
        result.sort(key=lambda r: r.get(field, None), reverse=reverse)

    # Project selected fields
    projected = []
    for row in result:
        new_row = {}
        for f in fields:
            if f not in row:
                raise ValueError(f"Field '{f}' not found in data rows")
            new_row[f] = row[f]
        projected.append(new_row)

    return projected
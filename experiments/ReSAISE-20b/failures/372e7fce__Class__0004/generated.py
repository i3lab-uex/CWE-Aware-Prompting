import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual operator functions
_OP_MAP = {
    '=': operator.eq,
    '==': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Supported logical operators for simple conditions
_LOGICAL_MAP = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}


def _parse_select_fields(select_part: str) -> List[str]:
    """Parse the SELECT part into a list of field names."""
    fields = [f.strip() for f in select_part.split(',')]
    if len(fields) == 1 and fields[0] == '*':
        return ['*']
    for f in fields:
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', f):
            raise ValueError(f"Invalid field name: {f}")
    return fields


def _tokenize_where(where_part: str) -> List[str]:
    """Tokenise the WHERE clause into a list of tokens."""
    # Simplistic tokenizer: splits on spaces but keeps quoted strings together
    pattern = r'''('[^']*'|"[^"]*"|\S+)'''
    tokens = re.findall(pattern, where_part)
    return [t.strip() for t in tokens if t]


def _parse_condition(tokens: List[str]) -> Any:
    """Parse a list of tokens into a lambda that evaluates the condition."""
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Handle simple conditions like field op value
    if len(tokens) == 3:
        field, op_token, value = tokens
        if op_token not in _OP_MAP:
            raise ValueError(f"Unsupported operator: {op_token}")
        op_func = _OP_MAP[op_token]
        # Remove quotes from string literals
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        else:
            # Try to interpret as number
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # keep as string
        return lambda record: op_func(record.get(field), value)

    # Handle compound conditions with AND/OR
    def eval_tokens(toks):
        if len(toks) < 3:
            raise ValueError("Invalid condition syntax")
        # Parse left side
        left = _parse_condition(toks[:3])
        if len(toks) == 3:
            return left
        # Expect logical operator next
        op_token = toks[3].upper()
        if op_token not in _LOGICAL_MAP:
            raise ValueError(f"Unsupported logical operator: {op_token}")
        right = eval_tokens(toks[4:])
        return lambda record: _LOGICAL_MAP[op_token](left(record), right(record))

    return eval_tokens(tokens)


def _apply_order_by(records: List[Dict[str, Any]], order_part: str) -> List[Dict[str, Any]]:
    """Sort records based on ORDER BY clause."""
    parts = [p.strip() for p in order_part.split(',')]
    sort_keys = []
    reverse_flags = []

    for part in parts:
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*(ASC|DESC)?$', part, re.IGNORECASE)
        if not m:
            raise ValueError(f"Invalid ORDER BY field: {part}")
        field, order = m.group(1), m.group(2)
        sort_keys.append(field)
        reverse_flags.append(order and order.upper() == 'DESC')

    def sort_key(record):
        return tuple(record.get(k) for k in sort_keys)

    # Python's sorted does not support multiple reverse flags directly,
    # so we perform successive sorts from last key to first.
    for field, rev in reversed(list(zip(sort_keys, reverse_flags))):
        records.sort(key=lambda r: r.get(field), reverse=rev)

    return records


def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Supported syntax:
        SELECT <fields> FROM <dataset_name>
        [WHERE <condition>]
        [ORDER BY <field1> [ASC|DESC], <field2> ...];

    Parameters
    ----------
    dataset_list : list of dict
        The data to query.
    sql_query : str
        SQL-like statement.

    Returns
    -------
    list of dict
        Query result.

    Raises
    ------
    ValueError
        If the query is malformed or unsupported.
    """
    if not isinstance(dataset_list, list) or not all(isinstance(r, dict) for r in dataset_list):
        raise ValueError("dataset_list must be a list of dictionaries")

    # Normalize query: strip semicolons and whitespace
    query = sql_query.strip().rstrip(';')
    # Basic regex to split into clauses
    pattern = re.compile(
        r'''
        SELECT\s+(?P<select>.+?)\s+FROM\s+(?P<from>\w+)
        (?:\s+WHERE\s+(?P<where>.+?))?
        (?:\s+ORDER\s+BY\s+(?P<order>.+?))?
        ''',
        re.IGNORECASE | re.VERBOSE
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Query syntax is invalid or unsupported")

    select_part = match.group('select')
    where_part = match.group('where')
    order_part = match.group('order')

    # SELECT
    fields = _parse_select_fields(select_part)

    # WHERE
    if where_part:
        tokens = _tokenize_where(where_part)
        condition_func = _parse_condition(tokens)
        filtered = [rec for rec in dataset_list if condition_func(rec)]
    else:
        filtered = list(dataset_list)

    # ORDER BY
    if order_part:
        filtered = _apply_order_by(filtered, order_part)

    # Projection
    if fields == ['*']:
        result = filtered
    else:
        result = []
        for rec in filtered:
            projected = {f: rec.get(f) for f in fields}
            result.append(projected)

    return result
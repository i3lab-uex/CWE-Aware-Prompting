import re
import operator
from functools import reduce

# Mapping of string operators to actual functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}

# Supported logical connectors
LOGICAL = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}


def _parse_condition(cond_str):
    """
    Parse a simple condition string into a callable that takes a record
    and returns True/False.
    Supports chained conditions with AND / OR (no parentheses).
    Example: "age >= 30 AND city = 'NY'"
    """
    tokens = re.split(r'\s+(AND|OR)\s+', cond_str.strip(), flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    # Build list of (condition, connector) tuples
    cond_funcs = []
    connectors = []

    # First token is a condition
    for i, tok in enumerate(tokens):
        if i % 2 == 0:  # condition
            cond_funcs.append(_parse_single_condition(tok))
        else:
            connectors.append(tok.upper())

    def evaluator(record):
        result = cond_funcs[0](record)
        for op, func in zip(connectors, cond_funcs[1:]):
            result = LOGICAL[op](result, func(record))
        return result

    return evaluator


def _parse_single_condition(cond):
    """
    Parse a single condition like "age >= 30" or "name = 'John'".
    Returns a function(record) -> bool.
    """
    match = re.match(r"(?P<field>\w+)\s*(?P<op>=|!=|<=|<|>=|>)\s*(?P<value>.+)", cond)
    if not match:
        raise ValueError(f"Invalid condition: {cond}")

    field = match.group('field')
    op_str = match.group('op')
    raw_value = match.group('value').strip()

    # Try to interpret value as int, float, or strip quotes
    if (raw_value.startswith("'") and raw_value.endswith("'")) or \
       (raw_value.startswith('"') and raw_value.endswith('"')):
        value = raw_value[1:-1]
    else:
        try:
            if '.' in raw_value:
                value = float(raw_value)
            else:
                value = int(raw_value)
        except ValueError:
            # Treat as string if not numeric
            value = raw_value

    op_func = OPERATORS[op_str]

    return lambda record: op_func(record.get(field), value)


def _parse_order_by(order_str):
    """
    Parse ORDER BY clause. Supports comma separated fields with optional ASC/DESC.
    Example: "age DESC, name"
    Returns a list of (field, reverse) tuples.
    """
    parts = [p.strip() for p in order_str.split(',')]
    orders = []
    for part in parts:
        tokens = part.split()
        field = tokens[0]
        reverse = False
        if len(tokens) > 1:
            if tokens[1].upper() == 'DESC':
                reverse = True
        orders.append((field, reverse))
    return orders


def run_user_query(dataset, sql_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    sql_query : str
        Query string. Supported syntax:
            SELECT <columns> [WHERE <condition>] [ORDER BY <fields>]

        * <columns> : comma separated field names or '*'
        * <condition> : simple comparison using =, !=, <, <=, >, >=
                        can chain with AND / OR (no parentheses)
        * <fields> : comma separated field names, optional ASC/DESC

    Returns
    -------
    list[dict]
        The query result.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("dataset must be a list of dictionaries")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in dataset must be dictionaries")

    # Basic regex to capture SELECT, optional WHERE and ORDER BY
    pattern = re.compile(
        r"SELECT\s+(?P<select>[\w\*,\s]+)"
        r"(?:\s+WHERE\s+(?P<where>[^ORDER]*))?"
        r"(?:\s+ORDER\s+BY\s+(?P<order>.+))?",
        re.IGNORECASE
    )
    match = pattern.fullmatch(sql_query.strip())
    if not match:
        raise ValueError("Invalid query format")

    select_part = match.group('select').strip()
    where_part = match.group('where')
    order_part = match.group('order')

    # Determine selected columns
    if select_part == '*':
        selected_columns = None  # all fields
    else:
        selected_columns = [col.strip() for col in select_part.split(',')]
        if not all(selected_columns):
            raise ValueError("Empty column name in SELECT clause")

    # Filter dataset if WHERE clause exists
    result = dataset
    if where_part:
        condition_func = _parse_condition(where_part.strip())
        try:
            result = list(filter(condition_func, result))
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Order results if ORDER BY clause exists
    if order_part:
        orders = _parse_order_by(order_part.strip())
        try:
            for field, reverse in reversed(orders):
                result.sort(key=lambda r: r.get(field), reverse=reverse)
        except Exception as e:
            raise ValueError(f"Error in ORDER BY clause: {e}")

    # Project selected columns
    if selected_columns is not None:
        try:
            result = [
                {col: rec.get(col) for col in selected_columns}
                for rec in result
            ]
        except Exception as e:
            raise ValueError(f"Error projecting columns: {e}")

    return result
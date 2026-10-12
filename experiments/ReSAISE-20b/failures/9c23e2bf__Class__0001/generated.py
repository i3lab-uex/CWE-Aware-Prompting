import re
import operator
from functools import reduce

# Mapping of comparison operators to Python functions
_COMPARATORS = {
    "=": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

# Allowed logical operators
_LOGICAL_OPS = {"AND", "OR"}


def _parse_where_clause(where_str: str):
    """
    Very small parser that turns a WHERE clause into a list of (field, op, value) tuples.
    Supports simple conditions combined with AND/OR (no parentheses).
    """
    tokens = re.findall(r"(\w+|\S)", where_str)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    conditions = []
    i = 0
    while i < len(tokens):
        # field
        if not re.match(r"\w+", tokens[i]):
            raise ValueError(f"Expected field name at token {i+1}")
        field = tokens[i]
        i += 1

        # operator
        if i >= len(tokens) or tokens[i] not in _COMPARATORS:
            raise ValueError(f"Expected comparison operator after field '{field}'")
        op_token = tokens[i]
        comp_func = _COMPARATORS[op_token]
        i += 1

        # value
        if i >= len(tokens):
            raise ValueError(f"Missing value for condition on field '{field}'")
        value_token = tokens[i]
        # Try to interpret as int or float, else keep string
        try:
            value = int(value_token)
        except ValueError:
            try:
                value = float(value_token)
            except ValueError:
                # strip quotes if present
                value = re.sub(r"^['\"]|['\"]$", "", value_token)
        i += 1

        conditions.append((field, comp_func, value))

        # Logical operator
        if i < len(tokens):
            if tokens[i] in _LOGICAL_OPS:
                conditions.append(tokens[i])
                i += 1
            else:
                raise ValueError(f"Unexpected token '{tokens[i]}' in WHERE clause")

    return conditions


def _evaluate_conditions(record, conditions):
    """
    Evaluate the list of conditions (including AND/OR) against a single record.
    """
    if not conditions:
        return True

    # Transform to RPN for simple evaluation
    output = []
    ops_stack = []

    precedence = {"AND": 2, "OR": 1}
    for token in conditions:
        if isinstance(token, tuple):
            output.append(token)
        elif token in _LOGICAL_OPS:
            while ops_stack and precedence[ops_stack[-1]] >= precedence[token]:
                output.append(ops_stack.pop())
            ops_stack.append(token)
        else:
            raise ValueError(f"Unknown token {token}")

    while ops_stack:
        output.append(ops_stack.pop())

    # Evaluate RPN
    stack = []
    for token in output:
        if isinstance(token, tuple):
            field, comp_func, value = token
            stack.append(comp_func(record.get(field), value))
        else:  # logical operator
            right = stack.pop()
            left = stack.pop()
            if token == "AND":
                stack.append(left and right)
            else:  # OR
                stack.append(left or right)

    return stack[0]


def run_custom_query(dataset, query):
    """
    Execute a very limited SQL‑like query on a list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        The data to query.
    query : str
        Query string, e.g. "SELECT name, age WHERE age > 30 ORDER BY age DESC".

    Returns
    -------
    list[dict]
        The filtered and sorted result set.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("dataset must be a list of dictionaries")

    # Basic regex to split SELECT, WHERE, ORDER BY
    pattern = r"""
        ^\s*SELECT\s+(?P<select>[^WHEREORDER]+?)            # SELECT clause
        (?:\s+WHERE\s+(?P<where>[^ORDER]+?) )?             # optional WHERE
        (?:\s+ORDER\s+BY\s+(?P<order>.+?) )?               # optional ORDER BY
        \s*$
    """
    match = re.match(pattern, query, re.IGNORECASE | re.VERBOSE)
    if not match:
        raise ValueError("Query format is invalid")

    select_clause = match.group('select').strip()
    where_clause = match.group('where')
    order_clause = match.group('order')

    # Parse SELECT
    if select_clause == "*":
        selected_fields = None  # all fields
    else:
        selected_fields = [f.strip() for f in select_clause.split(",")]
        if not all(selected_fields):
            raise ValueError("Empty field name in SELECT clause")

    # Parse WHERE
    if where_clause:
        conditions = _parse_where_clause(where_clause.strip())
    else:
        conditions = []

    # Filter records
    filtered = [rec for rec in dataset if _evaluate_conditions(rec, conditions)]

    # Order BY
    if order_clause:
        parts = [p.strip() for p in order_clause.split(",")]
        # Build sort key
        def sort_key(rec):
            keys = []
            for part in parts:
                if ' ' in part:
                    field, dir_ = part.rsplit(' ', 1)
                else:
                    field, dir_ = part, 'ASC'
                dir_ = dir_.upper()
                if field not in rec:
                    raise ValueError(f"Field '{field}' not found for ORDER BY")
                val = rec[field]
                # For descending order, invert value by using tuple (1, val) vs (-1, val)
                keys.append((0 if dir_ == 'ASC' else 1, val))
            return tuple(keys)

        filtered.sort(key=sort_key)
    # Select fields
    if selected_fields is not None:
        result = [{k: rec.get(k) for k in selected_fields} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]

    return result
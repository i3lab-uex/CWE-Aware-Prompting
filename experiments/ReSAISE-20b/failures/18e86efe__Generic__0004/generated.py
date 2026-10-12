import re
import operator
from functools import reduce

# Map string operators to functions
OPERATORS = {
    '==': operator.eq,
    '=':  operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>':  operator.gt,
    '<':  operator.lt,
}

def _parse_value(val: str):
    """Convert a string token into an int, float or stripped string."""
    val = val.strip()
    # Handle quoted strings
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    # Try int
    try:
        return int(val)
    except ValueError:
        pass
    # Try float
    try:
        return float(val)
    except ValueError:
        pass
    # Fallback: unquoted string
    return val

def _parse_condition(cond_str):
    """
    Parse a simple condition like "age >= 30" into (field, op_func, value).
    """
    pattern = r'^\s*(\w+)\s*([!<>=]{1,2})\s*(.+?)\s*$'
    m = re.match(pattern, cond_str)
    if not m:
        raise ValueError(f"Invalid condition syntax: '{cond_str}'")
    field, op_sym, val = m.groups()
    if op_sym not in OPERATORS:
        raise ValueError(f"Unsupported operator '{op_sym}'")
    return field, OPERATORS[op_sym], _parse_value(val)

def _evaluate_where(record, where_clause):
    """
    Evaluate a WHERE clause that may contain AND/OR.
    Supports only simple conditions combined with AND or OR, no parentheses.
    """
    # Split by AND/OR keeping operators
    tokens = re.split(r'\s+(AND|OR)\s+', where_clause, flags=re.IGNORECASE)
    if not tokens:
        return True

    # tokens will be like [cond1, op1, cond2, op2, ...]
    def eval_cond(cond):
        field, op_func, val = _parse_condition(cond)
        if field not in record:
            raise ValueError(f"Field '{field}' not found in dataset")
        return op_func(record[field], val)

    # Start evaluating
    result = eval_cond(tokens[0])
    i = 1
    while i < len(tokens):
        logical_op = tokens[i].upper()
        next_cond = eval_cond(tokens[i + 1])
        if logical_op == 'AND':
            result = result and next_cond
        elif logical_op == 'OR':
            result = result or next_cond
        else:
            raise ValueError(f"Unsupported logical operator '{logical_op}'")
        i += 2
    return result

def _parse_order_by(order_str):
    """
    Parse ORDER BY clause into list of (field, reverse) tuples.
    """
    orders = []
    for part in order_str.split(','):
        part = part.strip()
        if not part:
            continue
        tokens = part.split()
        field = tokens[0]
        direction = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Unsupported ORDER BY direction '{direction}'")
        orders.append((field, direction == 'DESC'))
    return orders

def run_user_query(dataset, sql_query):
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Parameters
    ----------
    dataset : list[dict]
        List of records.
    sql_query : str
        Query string.

    Returns
    -------
    list[dict]
        Result of the query execution.

    Raises
    ------
    ValueError
        If the query format is invalid or execution fails.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries.")
    if not all(isinstance(r, dict) for r in dataset):
        raise ValueError("All items in the dataset must be dictionaries.")

    # Normalize query: strip whitespace, remove trailing semicolon
    query = sql_query.strip().rstrip(';')
    # Regex to capture SELECT, WHERE and optional ORDER BY
    pattern = (
        r'^\s*SELECT\s+(?P<select>.+?)\s+'
        r'(?:WHERE\s+(?P<where>.*?))?\s*'
        r'(?:ORDER\s+BY\s+(?P<order>.*))?\s*$'
    )
    m = re.match(pattern, query, flags=re.IGNORECASE)
    if not m:
        raise ValueError("Query syntax is invalid.")

    select_part = m.group('select').strip()
    where_part = m.group('where')
    order_part = m.group('order')

    # Determine selected columns
    if select_part == '*':
        selected_cols = None  # all fields
    else:
        selected_cols = [col.strip() for col in select_part.split(',')]
        if not all(selected_cols):
            raise ValueError("Empty column name detected in SELECT clause.")

    # Filter dataset
    if where_part:
        filtered = [rec for rec in dataset if _evaluate_where(rec, where_part)]
    else:
        filtered = list(dataset)

    # Project columns
    if selected_cols is not None:
        result = []
        for rec in filtered:
            projected = {}
            for col in selected_cols:
                if col not in rec:
                    raise ValueError(f"Column '{col}' does not exist in dataset.")
                projected[col] = rec[col]
            result.append(projected)
    else:
        # Return deep copy to avoid accidental mutation
        result = [dict(rec) for rec in filtered]

    # Order the results if ORDER BY is present
    if order_part:
        orders = _parse_order_by(order_part)
        # Build a composite key function
        def sort_key(rec):
            return tuple(
                rec.get(field) for field, _ in orders
            )
        # Sort with reverse flag per column
        for field, reverse in reversed(orders):
            result.sort(key=lambda r: r.get(field), reverse=reverse)

    return result
import re
import operator
from functools import reduce

# Mapping of string operators to actual Python functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

# Logical operators
LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b,
}

def _parse_select_clause(sql):
    """Parse SELECT clause and return list of fields."""
    match = re.search(r"SELECT\s+(.*?)\s+WHERE|$",
                      sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("SELECT clause missing or malformed")
    fields = [f.strip() for f in match.group(1).split(',')]
    return fields

def _parse_where_clause(sql):
    """Parse WHERE clause and return list of conditions."""
    match = re.search(r"WHERE\s+(.*?)(?:ORDER BY|$)",
                      sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []  # No WHERE clause
    condition_str = match.group(1).strip()
    if not condition_str:
        return []
    # Split on AND/OR while keeping them as tokens
    tokens = re.split(r"(\bAND\b|\bOR\b)", condition_str, flags=re.IGNORECASE)
    tokens = [t.strip() for t in tokens if t.strip()]
    return tokens

def _parse_order_by_clause(sql):
    """Parse ORDER BY clause and return list of (field, direction)."""
    match = re.search(r"ORDER\s+BY\s+(.*)$",
                      sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []  # No ORDER BY
    order_str = match.group(1).strip()
    orders = []
    for part in order_str.split(','):
        parts = part.strip().split()
        field = parts[0]
        direction = parts[1].upper() if len(parts) > 1 else 'ASC'
        if direction not in ('ASC', 'DESC'):
            raise ValueError(f"Unknown ORDER BY direction: {direction}")
        orders.append((field, direction))
    return orders

def _evaluate_condition(record, condition):
    """Evaluate a simple comparison condition like `age >= 30`."""
    # Regex to capture left operand, operator, right operand
    m = re.match(r"(\w+)\s*(=|!=|<>|>=|<=|>|<)\s*([^\s]+)", condition)
    if not m:
        raise ValueError(f"Unsupported or malformed condition: {condition}")
    field, op_str, value = m.groups()
    if field not in record:
        raise ValueError(f"Field {field} does not exist in the dataset")
    # Convert value to appropriate type if possible
    try:
        if isinstance(record[field], int):
            value = int(value)
        elif isinstance(record[field], float):
            value = float(value)
    except ValueError:
        # Keep as string
        pass
    op_func = OPERATORS[op_str]
    return op_func(record[field], value)

def _apply_where(dataset, where_tokens):
    """Apply WHERE conditions to the dataset."""
    if not where_tokens:
        return dataset
    # Build a function that evaluates the entire expression
    def predicate(record):
        stack = []
        for token in where_tokens:
            if token.upper() in LOGICAL_OPERATORS:
                # Logical operator: combine last two results
                if len(stack) < 2:
                    raise ValueError("Malformed logical expression")
                b = stack.pop()
                a = stack.pop()
                op_func = LOGICAL_OPERATORS[token.upper()]
                stack.append(op_func(a, b))
            else:
                # It's a condition
                stack.append(_evaluate_condition(record, token))
        if len(stack) != 1:
            raise ValueError("Malformed WHERE clause")
        return stack[0]
    try:
        return list(filter(predicate, dataset))
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}")

def _apply_order_by(dataset, order_specs):
    """Sort dataset based on ORDER BY specifications."""
    if not order_specs:
        return dataset
    def sort_key(record):
        key = []
        for field, direction in order_specs:
            val = record.get(field)
            # None values should come last
            key.append((val is None, val))
        return key
    reverse = any(direction == 'DESC' for _, direction in order_specs)
    try:
        return sorted(dataset, key=sort_key, reverse=reverse)
    except Exception as e:
        raise ValueError(f"Error applying ORDER BY: {e}")

def _apply_select(dataset, fields):
    """Project selected fields from dataset."""
    if not fields or fields == ['*']:
        return dataset
    result = []
    for record in dataset:
        new_rec = {}
        for f in fields:
            if f not in record:
                raise ValueError(f"Field {f} does not exist in the dataset")
            new_rec[f] = record[f]
        result.append(new_rec)
    return result

def run_sql_query(dataset, sql_query):
    """
    Execute a simplified SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : list[dict]
        List of dictionaries representing rows.
    sql_query : str
        SQL-like query string.

    Returns
    -------
    list[dict]
        Resulting rows after applying SELECT, WHERE, ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset, list) or any(not isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("SQL query must be a string")

    # Normalize whitespace
    sql = re.sub(r'\s+', ' ', sql_query.strip())

    try:
        fields = _parse_select_clause(sql)
        where_tokens = _parse_where_clause(sql)
        order_specs = _parse_order_by_clause(sql)

        # Apply clauses
        filtered = _apply_where(dataset, where_tokens)
        ordered = _apply_order_by(filtered, order_specs)
        selected = _apply_select(ordered, fields)

        return selected
    except Exception as e:
        raise ValueError(f"Failed to execute query: {e}") from None
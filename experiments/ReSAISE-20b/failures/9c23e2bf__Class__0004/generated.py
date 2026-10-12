import re
import operator
from functools import reduce

# Mapping of supported operators to their functions
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Regex patterns for parsing the query
SELECT_PATTERN = re.compile(
    r"^\s*SELECT\s+(?P<fields>[\*\w,\s]+)\s+FROM\s+\w+\s*(WHERE\s+(?P<where>.+?)\s*)?(ORDER\s+BY\s+(?P<orderby>[\w,\s]+)\s*)?$",
    re.IGNORECASE
)

WHERE_CLAUSE_PATTERN = re.compile(
    r"(?P<field>\w+)\s*(?P<op>=|!=|<>|>|<|>=|<=)\s*'(?P<value>[^']*)'", re.IGNORECASE
)

def _parse_query(query: str):
    """Parse the query and return its components."""
    match = SELECT_PATTERN.match(query)
    if not match:
        raise ValueError("Invalid query format")

    fields = [f.strip() for f in match.group('fields').split(',')]
    if len(fields) == 1 and fields[0] == '*':
        fields = None  # Means all fields

    where_clause = match.group('where')
    order_by = match.group('orderby')

    return fields, where_clause, order_by

def _evaluate_where(record: dict, clause: str):
    """Evaluate a simple WHERE clause against a record."""
    # Currently supports only single condition for simplicity
    match = WHERE_CLAUSE_PATTERN.match(clause.strip())
    if not match:
        raise ValueError(f"Unsupported WHERE clause: {clause}")

    field = match.group('field')
    op_str = match.group('op')
    value_raw = match.group('value')

    if field not in record:
        return False

    op_func = OPERATORS.get(op_str)
    if not op_func:
        raise ValueError(f"Unsupported operator: {op_str}")

    # Attempt to cast value to the same type as record's field
    rec_value = record[field]
    try:
        # Try int conversion if possible
        if isinstance(rec_value, int):
            value = int(value_raw)
        elif isinstance(rec_value, float):
            value = float(value_raw)
        else:
            value = value_raw
    except ValueError:
        value = value_raw

    return op_func(rec_value, value)

def _apply_order_by(dataset: list, order_by: str):
    """Sort the dataset based on ORDER BY clause."""
    fields = [f.strip() for f in order_by.split(',')]
    # For now, support ascending only
    return sorted(dataset, key=lambda r: tuple(r.get(f) for f in fields))

def run_custom_query(dataset: list, query: str) -> list:
    """
    Execute a basic SQL-like SELECT statement on the provided dataset.

    Parameters
    ----------
    dataset : list[dict]
        The data records to query.
    query : str
        SQL-like statement (SELECT ... FROM ... [WHERE ...] [ORDER BY ...]).

    Returns
    -------
    list[dict]
        The result set after applying SELECT, WHERE, and ORDER BY.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be processed.
    """
    if not isinstance(dataset, list) or not all(isinstance(r, dict) for r in dataset):
        raise ValueError("Dataset must be a list of dictionaries")

    fields, where_clause, order_by = _parse_query(query)

    # Apply WHERE filtering
    if where_clause:
        try:
            filtered = [rec for rec in dataset if _evaluate_where(rec, where_clause)]
        except Exception as exc:
            raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc
    else:
        filtered = list(dataset)

    # Apply ORDER BY sorting
    if order_by:
        try:
            filtered = _apply_order_by(filtered, order_by)
        except Exception as exc:
            raise ValueError(f"Error applying ORDER BY: {exc}") from exc

    # Apply SELECT field projection
    if fields is not None:
        result = []
        for rec in filtered:
            projected = {f: rec.get(f) for f in fields}
            result.append(projected)
    else:
        result = filtered

    return result
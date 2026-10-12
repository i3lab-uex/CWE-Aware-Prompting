import re
import operator
from functools import reduce

# Supported operators for WHERE clauses
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}

# Regex patterns for parsing the SQL-like query
SELECT_PATTERN = re.compile(
    r"^\s*SELECT\s+(?P<select>[\*\w,\s]+)\s+FROM\s+\w+\s*(WHERE\s+(?P<where>.+?))?\s*(ORDER\s+BY\s+(?P<order_by>\w+)\s*(?P<order_dir>ASC|DESC)?)?\s*;\s*$",
    re.IGNORECASE
)

# Regex pattern for individual conditions in WHERE clause (very simple, no parentheses)
COND_PATTERN = re.compile(
    r"(?P<field>\w+)\s*(?P<op>=|!=|<=|>=|<|>)\s*(?P<value>[^=<>!]+)",
    re.IGNORECASE
)


def _parse_where(where_clause: str):
    """
    Parse a simple WHERE clause into a list of (field, operator_func, value) tuples.
    Only supports AND between conditions.
    """
    if not where_clause:
        return []

    # Split on AND (case-insensitive)
    parts = [p.strip() for p in re.split(r'\bAND\b', where_clause, flags=re.IGNORECASE)]
    conditions = []
    for part in parts:
        match = COND_PATTERN.fullmatch(part)
        if not match:
            raise ValueError(f"Invalid WHERE condition: {part}")
        field = match.group('field')
        op_str = match.group('op')
        value_raw = match.group('value').strip()
        # Try to interpret numeric values
        try:
            value = int(value_raw)
        except ValueError:
            try:
                value = float(value_raw)
            except ValueError:
                # Remove surrounding quotes if present
                if (value_raw.startswith("'") and value_raw.endswith("'")) or \
                   (value_raw.startswith('"') and value_raw.endswith('"')):
                    value = value_raw[1:-1]
                else:
                    value = value_raw
        op_func = OPERATORS.get(op_str)
        if not op_func:
            raise ValueError(f"Unsupported operator: {op_str}")
        conditions.append((field, op_func, value))
    return conditions


def _apply_where(record: dict, conditions):
    """
    Return True if the record satisfies all conditions.
    """
    for field, op_func, value in conditions:
        if field not in record:
            return False
        try:
            if not op_func(record[field], value):
                return False
        except Exception as e:
            raise ValueError(f"Error evaluating condition on field '{field}': {e}")
    return True


def _parse_select(select_clause: str):
    """
    Parse SELECT clause into list of fields.
    '*' means all fields.
    """
    if select_clause.strip() == '*':
        return None  # None indicates all fields
    fields = [f.strip() for f in select_clause.split(',')]
    if not all(fields):
        raise ValueError("Empty field name detected in SELECT clause.")
    return fields


def _apply_select(record: dict, fields):
    """
    Return a new record containing only the selected fields.
    If fields is None, return original record.
    """
    if fields is None:
        return record
    return {f: record.get(f) for f in fields}


def handle_sql_query(records, sql_command):
    """
    Execute a simple SQL-like query on the provided list of record dictionaries.

    Parameters
    ----------
    records : list[dict]
        The dataset to query.
    sql_command : str
        A string containing the SQL-like query. Must end with a semicolon.

    Returns
    -------
    list[dict]
        The result of the query as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list of dictionaries.")
    if not all(isinstance(r, dict) for r in records):
        raise ValueError("All items in records must be dictionaries.")

    match = SELECT_PATTERN.fullmatch(sql_command)
    if not match:
        raise ValueError("Query does not conform to supported syntax.")

    select_clause = match.group('select')
    where_clause = match.group('where')
    order_by_field = match.group('order_by')
    order_dir = match.group('order_dir') or 'ASC'

    # Parse SELECT fields
    select_fields = _parse_select(select_clause)

    # Parse WHERE conditions
    where_conditions = _parse_where(where_clause)

    # Filter records
    filtered = [rec for rec in records if _apply_where(rec, where_conditions)]

    # Apply SELECT projection
    projected = [_apply_select(rec, select_fields) for rec in filtered]

    # Order BY if specified
    if order_by_field:
        reverse = order_dir.upper() == 'DESC'
        try:
            projected.sort(key=lambda r: r.get(order_by_field), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by field '{order_by_field}': {e}")

    return projected
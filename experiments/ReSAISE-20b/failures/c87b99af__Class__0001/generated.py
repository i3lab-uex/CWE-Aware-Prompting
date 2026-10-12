import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual Python operator functions
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,   # SQL equivalent of NOT EQUAL
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

# Allowed functions for ORDER BY (only ascending/descending)
_ORDER_MAP = {
    'ASC': False,   # False indicates no reverse
    'DESC': True,
}

def _parse_select_clause(clause: str) -> List[str]:
    """Parse the SELECT clause into a list of column names."""
    columns = [col.strip() for col in clause.split(',')]
    if not all(columns):
        raise ValueError("Empty column name in SELECT clause")
    return columns

def _parse_where_clause(clause: str) -> List[tuple]:
    """Parse the WHERE clause into a list of (field, op, value) tuples."""
    # Simple regex: field operator value
    pattern = re.compile(r"""
        (?P<field>\w+)\s*
        (?P<op>=|!=|<>|>|<|>=|<=)\s*
        (?P<value>[^;]+)          # Anything until end of clause
    """, re.VERBOSE | re.IGNORECASE)
    matches = pattern.findall(clause)
    if not matches:
        raise ValueError("Invalid WHERE clause syntax")
    conditions = []
    for field, op, value in matches:
        # Strip quotes from string literals
        val = value.strip()
        if (val.startswith("'") and val.endswith("'")) or \
           (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]
        else:
            # Try to interpret as int or float
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                # Leave as string if conversion fails
                pass
        conditions.append((field, _OPERATOR_MAP[op.upper()], val))
    return conditions

def _apply_where(record: Dict[str, Any], conditions: List[tuple]) -> bool:
    """Return True if the record satisfies all WHERE conditions."""
    for field, op_func, value in conditions:
        # If the field is missing, treat as None
        record_value = record.get(field)
        if not op_func(record_value, value):
            return False
    return True

def _parse_order_by_clause(clause: str) -> List[tuple]:
    """Parse ORDER BY clause into list of (field, reverse) tuples."""
    orders = []
    for part in clause.split(','):
        tokens = part.strip().split()
        if not tokens:
            continue
        field = tokens[0]
        direction = tokens[1].upper() if len(tokens) > 1 else 'ASC'
        if direction not in _ORDER_MAP:
            raise ValueError(f"Unsupported ORDER BY direction: {direction}")
        orders.append((field, _ORDER_MAP[direction]))
    return orders

def execute_user_query(records: List[Dict[str, Any]], user_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on a list of dictionaries.

    Supported syntax:
        SELECT <columns> FROM data [WHERE <conditions>] [ORDER BY <fields>];

    Parameters:
        records (list): List of dictionaries representing the dataset.
        user_query (str): SQL-like query string.

    Returns:
        List[Dict]: Query result as a list of dictionaries.

    Raises:
        ValueError: If the query format is invalid or execution fails.
    """
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError("records must be a list of dictionaries")

    # Basic normalization
    query = user_query.strip().rstrip(';').strip()
    if not query.upper().startswith('SELECT '):
        raise ValueError("Only SELECT queries are supported")

    # Regex to extract clauses
    pattern = re.compile(
        r"""
        SELECT\s+(?P<select>[^FROM]+)\s+FROM\s+\w+
        (?:\s+WHERE\s+(?P<where>[^ORDER BY]+))?
        (?:\s+ORDER\s+BY\s+(?P<order>.+))?
        """,
        re.IGNORECASE | re.VERBOSE
    )
    match = pattern.fullmatch(query)
    if not match:
        raise ValueError("Query syntax is invalid")

    select_clause = match.group('select')
    where_clause = match.group('where')
    order_clause = match.group('order')

    # Parse SELECT
    selected_columns = _parse_select_clause(select_clause)

    # Filter records based on WHERE
    if where_clause:
        conditions = _parse_where_clause(where_clause)
        filtered = [r for r in records if _apply_where(r, conditions)]
    else:
        filtered = records[:]

    # Order results
    if order_clause:
        orders = _parse_order_by_clause(order_clause)
        # Build a key function that returns tuple of values
        def sort_key(rec: Dict[str, Any]):
            return tuple(
                rec.get(field) for field, _ in orders
            )
        # Since multiple directions may be specified, we perform stable sorts from last to first
        for field, reverse in reversed(orders):
            filtered.sort(key=lambda r: r.get(field), reverse=reverse)

    # Project selected columns
    result = []
    for rec in filtered:
        projected = {col: rec.get(col) for col in selected_columns}
        result.append(projected)

    return result
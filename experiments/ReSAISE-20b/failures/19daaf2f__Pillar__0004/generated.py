import re
import operator
from functools import reduce
from typing import List, Dict, Callable, Any

# Mapping of string operators to functions from operator module
OPERATORS = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,
    '>=': operator.ge,
    '<=': operator.le,
    '>': operator.gt,
    '<': operator.lt
}

LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}


def _parse_select_clause(clause: str) -> List[str]:
    """Parse the SELECT clause and return a list of columns."""
    cols = [c.strip() for c in clause.split(',')]
    if len(cols) == 1 and cols[0] == '*':
        return ['*']
    if any(not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', c) for c in cols):
        raise ValueError(f"Invalid column name in SELECT clause: {clause}")
    return cols


def _parse_order_by_clause(clause: str) -> List[tuple]:
    """Parse ORDER BY clause into a list of (column, ascending)."""
    parts = [p.strip() for p in clause.split(',')]
    orderings = []
    for part in parts:
        tokens = part.split()
        if len(tokens) == 1:
            col, asc = tokens[0], True
        elif len(tokens) == 2 and tokens[1].upper() in ('ASC', 'DESC'):
            col, asc = tokens[0], tokens[1].upper() == 'ASC'
        else:
            raise ValueError(f"Invalid ORDER BY syntax: {part}")
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col):
            raise ValueError(f"Invalid column name in ORDER BY: {col}")
        orderings.append((col, asc))
    return orderings


def _build_where_function(where_clause: str) -> Callable[[Dict[str, Any]], bool]:
    """
    Build a predicate function from the WHERE clause.
    Supports simple expressions combined with AND/OR (no parentheses).
    Example: "age > 30 AND name = 'John'"
    """
    # Tokenize the clause
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[<>!=]=?|'[^']*'|\S", where_clause)
    if not tokens:
        raise ValueError("Empty WHERE clause")

    def parse_condition(tok_index: int):
        # Parse left operand
        if tok_index >= len(tokens):
            raise ValueError("Malformed WHERE clause")
        left = tokens[tok_index]
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', left):
            raise ValueError(f"Invalid field name: {left}")
        # Operator
        if tok_index + 1 >= len(tokens):
            raise ValueError("Operator expected in WHERE clause")
        op_token = tokens[tok_index + 1]
        if op_token not in OPERATORS:
            raise ValueError(f"Unsupported operator: {op_token}")
        # Right operand
        if tok_index + 2 >= len(tokens):
            raise ValueError("Right-hand value expected in WHERE clause")
        right_token = tokens[tok_index + 2]
        if re.match(r"^'[^']*'$", right_token):
            right = right_token.strip("'")
        else:
            try:
                # Try to parse as int or float
                if '.' in right_token:
                    right = float(right_token)
                else:
                    right = int(right_token)
            except ValueError:
                raise ValueError(f"Unsupported literal: {right_token}")
        return left, OPERATORS[op_token], right, tok_index + 3

    # Build a list of simple conditions and logical operators
    conditions = []
    i = 0
    while i < len(tokens):
        left, op_func, right, next_i = parse_condition(i)
        conditions.append((left, op_func, right))
        i = next_i
        if i < len(tokens):
            logical_token = tokens[i].upper()
            if logical_token not in LOGICAL_OPERATORS:
                raise ValueError(f"Unsupported logical operator: {logical_token}")
            conditions.append(logical_token)
            i += 1

    # Convert to a single predicate function
    def predicate(row: Dict[str, Any]) -> bool:
        # Evaluate the first condition
        left, op_func, right = conditions[0]
        if left not in row:
            return False
        try:
            result = op_func(row[left], right)
        except Exception:
            return False
        # Evaluate subsequent conditions with logical operators
        idx = 1
        while idx < len(conditions):
            logical_op = conditions[idx]
            left, op_func, right = conditions[idx + 1]
            if left not in row:
                return False
            try:
                cond_val = op_func(row[left], right)
            except Exception:
                return False
            result = LOGICAL_OPERATORS[logical_op](result, cond_val)
            idx += 2
        return result

    return predicate


def run_sql_query(dataset: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset : List[Dict[str, Any]]
        The data to query. Each dictionary represents a row.
    sql_query : str
        A string containing the SQL-like query.

    Returns
    -------
    List[Dict[str, Any]]
        The result set as a list of dictionaries.

    Raises
    ------
    ValueError
        If the query is malformed or cannot be executed.
    """
    if not isinstance(dataset, list):
        raise ValueError("Dataset must be a list of dictionaries")
    if not isinstance(sql_query, str):
        raise ValueError("Query must be a string")

    # Normalize whitespace and upper-case keywords for parsing
    query = re.sub(r'\s+', ' ', sql_query.strip())
    # Regex to capture SELECT, FROM, WHERE, ORDER BY
    pattern = re.compile(
        r'^SELECT\s+(?P<select>.+?)\s+FROM\s+\S+'
        r'(?:\s+WHERE\s+(?P<where>.+?))?'
        r'(?:\s+ORDER\s+BY\s+(?P<order_by>.+))?$',
        re.IGNORECASE
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Query is not a supported SELECT statement")

    select_clause = match.group('select')
    where_clause = match.group('where')
    order_by_clause = match.group('order_by')

    # Parse SELECT
    selected_columns = _parse_select_clause(select_clause)

    # Build WHERE predicate if present
    where_predicate: Callable[[Dict[str, Any]], bool] = lambda row: True  # default always true
    if where_clause:
        where_predicate = _build_where_function(where_clause)

    # Filter rows
    try:
        filtered_rows = [row for row in dataset if where_predicate(row)]
    except Exception as e:
        raise ValueError(f"Error evaluating WHERE clause: {e}") from e

    # Parse ORDER BY if present
    if order_by_clause:
        ordering = _parse_order_by_clause(order_by_clause)
        for col, asc in reversed(ordering):
            try:
                filtered_rows.sort(key=lambda r: r.get(col, None), reverse=not asc)
            except Exception as e:
                raise ValueError(f"Error sorting by column '{col}': {e}") from e

    # Project selected columns
    result = []
    for row in filtered_rows:
        if selected_columns == ['*']:
            projected = dict(row)
        else:
            projected = {col: row.get(col) for col in selected_columns}
        result.append(projected)

    return result
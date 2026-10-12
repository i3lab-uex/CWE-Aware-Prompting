import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of string operators to actual functions
_OP_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,   # SQL standard for NOT EQUAL
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Supported logical operators
_LOGICAL_OPS = {'AND', 'OR'}


def _tokenize_where(condition: str) -> List[str]:
    """
    Split the WHERE condition into tokens while preserving string literals.
    """
    # Regex to match identifiers, operators, numbers, or quoted strings
    token_pattern = re.compile(r"""
        \s*(?:
            (?P<identifier>[a-zA-Z_][a-zA-Z0-9_]*) |
            (?P<operator>!=|<>|>=|<=|=|>|<) |
            (?P<number>\d+(?:\.\d+)?) |
            (?P<string>'[^']*'|"[^"]*") |
            (?P<logical>AND|OR)
        )
    """, re.VERBOSE | re.IGNORECASE)

    tokens = []
    pos = 0
    while pos < len(condition):
        match = token_pattern.match(condition, pos)
        if not match:
            raise ValueError(f"Invalid WHERE clause near: '{condition[pos:]}'")
        for key, value in match.groupdict().items():
            if value:
                tokens.append(value)
                break
        pos = match.end()
    return tokens


def _build_condition_func(tokens: List[str]) -> Any:
    """
    Convert a list of tokens into a callable that evaluates a record.
    Supports simple comparisons and logical AND/OR with left-to-right precedence.
    """
    def parse_expression(index: int):
        # Parse a single comparison expression
        if index + 2 >= len(tokens):
            raise ValueError("Incomplete condition in WHERE clause")
        left = tokens[index]
        op_token = tokens[index + 1]
        right = tokens[index + 2]

        if op_token not in _OP_MAP:
            raise ValueError(f"Unsupported operator '{op_token}' in WHERE clause")

        # Resolve right operand value
        if re.match(r"^'.*'$|^\".*\"$", right):
            # Strip quotes
            value = right[1:-1]
        elif re.match(r'^\d+(\.\d+)?$', right):
            value = float(right) if '.' in right else int(right)
        else:
            # Assume field reference; value will be looked up later
            value = right

        def expr(record):
            left_val = record.get(left)
            # If the right side is a field reference, look it up
            if isinstance(value, str) and value not in record:
                right_val = value
            else:
                right_val = value
            return _OP_MAP[op_token](left_val, right_val)

        return expr, index + 3

    # Build leftmost expression
    func_stack = []
    idx = 0
    expr, idx = parse_expression(idx)
    func_stack.append(expr)

    # Process remaining tokens
    while idx < len(tokens):
        logical_op = tokens[idx].upper()
        if logical_op not in _LOGICAL_OPS:
            raise ValueError(f"Unsupported logical operator '{logical_op}'")
        idx += 1
        next_expr, idx = parse_expression(idx)
        # Combine previous and next expressions
        if logical_op == 'AND':
            prev = func_stack.pop()
            combined = lambda rec, p=prev, n=next_expr: p(rec) and n(rec)
        else:  # OR
            prev = func_stack.pop()
            combined = lambda rec, p=prev, n=next_expr: p(rec) or n(rec)
        func_stack.append(combined)

    if len(func_stack) != 1:
        raise ValueError("Failed to parse WHERE clause")
    return func_stack[0]


def process_sql_request(dataset_records: List[Dict[str, Any]],
                        sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.

    Parameters
    ----------
    dataset_records : list[dict]
        The dataset to query.
    sql_statement : str
        A string containing the SQL-like query.

    Returns
    -------
    list[dict]
        The result set after applying SELECT, WHERE and ORDER BY clauses.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset_records, list) or \
       not all(isinstance(r, dict) for r in dataset_records):
        raise ValueError("dataset_records must be a list of dictionaries")

    # Basic regex to parse SELECT, WHERE, ORDER BY
    pattern = re.compile(
        r"""
        ^\s*SELECT\s+(?P<select>[\w,\s*]+)\s+
        (?:FROM\s+\w+\s+)?                     # Optional FROM clause
        (?:WHERE\s+(?P<where>[^;]+?)\s*)?      # Optional WHERE
        (?:ORDER\s+BY\s+(?P<order>[^;]+?)\s*)? # Optional ORDER BY
        ;?\s*$
        """,
        re.IGNORECASE | re.VERBOSE,
    )
    match = pattern.match(sql_statement)
    if not match:
        raise ValueError("SQL statement is malformed")

    select_clause = match.group('select').strip()
    where_clause = match.group('where')
    order_clause = match.group('order')

    # Determine selected columns
    if select_clause == '*':
        selected_cols = None  # All columns
    else:
        selected_cols = [col.strip() for col in select_clause.split(',')]
        if not all(selected_cols):
            raise ValueError("SELECT clause contains empty column names")

    # Filter records based on WHERE
    filtered = dataset_records
    if where_clause:
        tokens = _tokenize_where(where_clause)
        condition_func = _build_condition_func(tokens)
        try:
            filtered = [rec for rec in dataset_records if condition_func(rec)]
        except Exception as e:
            raise ValueError(f"Error evaluating WHERE clause: {e}")

    # Sort records based on ORDER BY
    if order_clause:
        order_cols = [col.strip() for col in order_clause.split(',')]
        if not all(order_cols):
            raise ValueError("ORDER BY clause contains empty column names")
        try:
            filtered.sort(key=lambda rec: tuple(rec.get(col) for col in order_cols))
        except Exception as e:
            raise ValueError(f"Error evaluating ORDER BY clause: {e}")

    # Project selected columns
    result = []
    for rec in filtered:
        if selected_cols is None:
            projected = dict(rec)
        else:
            projected = {col: rec.get(col) for col in selected_cols}
        result.append(projected)

    return result
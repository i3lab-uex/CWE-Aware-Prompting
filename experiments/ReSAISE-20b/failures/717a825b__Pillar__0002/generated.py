import re
import operator as op
import functools
import ast
from typing import List, Dict, Any

# Mapping of supported operators from the query language to Python operators
OPERATORS = {
    '=': op.eq,
    '!=': op.ne,
    '<>': op.ne,
    '>': op.gt,
    '<': op.lt,
    '>=': op.ge,
    '<=': op.le,
}

LOGICAL_OPERATORS = {
    'AND': op.and_,
    'OR': op.or_,
}

# Whitelist of allowed AST node types for condition parsing
ALLOWED_NODES = {
    ast.Expression,
    ast.Compare,
    ast.BoolOp,
    ast.Name,
    ast.Constant,
    ast.BinOp,  # allow simple arithmetic if needed
    ast.UnaryOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.USub,
}

def _validate_condition_ast(node: ast.AST) -> None:
    """Recursively ensure that the AST contains only allowed node types."""
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _validate_condition_ast(child)

def _evaluate_condition(condition: str, row: Dict[str, Any]) -> bool:
    """
    Safely evaluate a condition string against a single row.
    Only allows names that exist in the row and basic comparison/logical ops.
    """
    # Replace SQL operators with Python equivalents
    condition = re.sub(r'\bAND\b', 'and', condition, flags=re.IGNORECASE)
    condition = re.sub(r'\bOR\b', 'or', condition, flags=re.IGNORECASE)
    # Ensure equality operator is ==
    condition = re.sub(r'(?<![=!<>])=(?!=)', '==', condition)
    # Replace <> with !=
    condition = re.sub(r'<>', '!=', condition)

    # Parse the expression to AST
    try:
        expr = ast.parse(condition, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid condition syntax: {e}")

    # Validate the AST
    _validate_condition_ast(expr)

    # Compile and evaluate with row as local namespace
    compiled = compile(expr, '<string>', 'eval')
    try:
        return bool(eval(compiled, {}, row))
    except Exception as e:
        raise ValueError(f"Failed to evaluate condition: {e}")

def execute_custom_query(data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like SELECT query on a list of dictionaries.

    Supported syntax:
        SELECT <columns>
        [WHERE <condition>]
        [ORDER BY <column1> [ASC|DESC], <column2> [ASC|DESC], ...]
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Data must be a list of dictionaries.")

    # Basic regex to capture clauses
    pattern = re.compile(
        r'''
        ^\s*SELECT\s+(?P<columns>[^WHEREORDER]*?)   # columns
        (?:\s+WHERE\s+(?P<where>[^ORDER]*?))?      # optional WHERE
        (?:\s+ORDER\s+BY\s+(?P<order>.+))?         # optional ORDER BY
        \s*$
        ''',
        re.IGNORECASE | re.VERBOSE,
    )
    match = pattern.match(query)
    if not match:
        raise ValueError("Query syntax is invalid.")

    columns_raw = match.group('columns').strip()
    where_clause = match.group('where')
    order_by_raw = match.group('order')

    # Parse selected columns
    if not columns_raw or columns_raw == '*':
        selected_columns = None  # all columns
    else:
        selected_columns = [col.strip() for col in columns_raw.split(',')]
        if not all(selected_columns):
            raise ValueError("Column names cannot be empty.")

    # Filter rows
    if where_clause:
        filtered = []
        for row in data:
            try:
                if _evaluate_condition(where_clause, row):
                    filtered.append(row)
            except ValueError as e:
                raise ValueError(f"Error evaluating WHERE clause: {e}")
    else:
        filtered = data[:]

    # Order rows
    if order_by_raw:
        order_parts = [part.strip() for part in order_by_raw.split(',')]
        sort_keys = []
        reverse_flags = []

        for part in order_parts:
            tokens = part.split()
            if not tokens:
                raise ValueError("Empty ORDER BY clause.")
            col = tokens[0]
            direction = 'ASC'
            if len(tokens) > 1:
                dir_token = tokens[1].upper()
                if dir_token in ('ASC', 'DESC'):
                    direction = dir_token
                else:
                    raise ValueError(f"Unknown sort direction: {dir_token}")
            if selected_columns and col not in selected_columns:
                # Column may be missing from selection but still used for ordering
                pass  # allow; will just ignore if not present in row
            sort_keys.append(col)
            reverse_flags.append(direction == 'DESC')

        # Build composite key function
        def sort_key(row):
            return tuple(row.get(k) for k in sort_keys)

        # Since Python's sorted doesn't support multiple reverse flags, we apply successive sorts
        for col, rev in reversed(list(zip(sort_keys, reverse_flags))):
            filtered.sort(key=lambda r: r.get(col), reverse=rev)

    # Project selected columns
    result = []
    for row in filtered:
        if selected_columns is None:
            projected = dict(row)  # shallow copy
        else:
            projected = {col: row.get(col) for col in selected_columns}
        result.append(projected)

    return result
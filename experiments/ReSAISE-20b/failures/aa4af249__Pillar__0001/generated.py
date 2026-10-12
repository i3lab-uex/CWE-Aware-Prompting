#!/usr/bin/env python3
"""
A minimal SQL‑like query processor for in‑memory data represented as a list of dictionaries.
Supported clauses: SELECT, WHERE, ORDER BY.

Author: ChatGPT
"""

import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Mapping of comparison operators to functions
_cmp_ops = {
    "=": operator.eq,
    "==": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

# Supported logical operators
_logical_ops = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
}


def _parse_select_clause(sql: str) -> List[str]:
    """
    Extract column names from the SELECT clause.
    """
    m = re.search(r"SELECT\s+(.*?)\s+FROM", sql, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        raise ValueError("SELECT clause missing or malformed")
    cols = [c.strip() for c in m.group(1).split(",")]
    if not all(cols):
        raise ValueError("Empty column name in SELECT clause")
    return cols


def _parse_where_clause(sql: str) -> List[str]:
    """
    Return a list of tokens representing the WHERE clause.
    Tokens are column names, literals, comparison operators and logical operators.
    """
    m = re.search(r"WHERE\s+(.*?)(ORDER BY|$)", sql, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return []  # No WHERE clause
    where_str = m.group(1).strip()
    if not where_str:
        raise ValueError("WHERE clause is empty")

    # Tokenize: split by spaces but keep quoted strings together
    token_pattern = r"""
        ('[^']*'|"[^"]*"|<=|>=|<>|!=|==|=|<|>|AND|OR|\w+)
    """
    tokens = re.findall(token_pattern, where_str, flags=re.IGNORECASE | re.VERBOSE)
    if not tokens:
        raise ValueError("Failed to parse WHERE clause")
    return [t.upper() if t.upper() in _logical_ops else t for t in tokens]


def _evaluate_condition(record: Dict[str, Any], tokens: List[str]) -> bool:
    """
    Evaluate the WHERE condition for a single record.
    Supports simple binary comparisons combined with AND/OR.
    """
    def _value(token: str):
        if token.startswith(("'", '"')) and token.endswith(("'", '"')):
            return token[1:-1]
        try:
            # Try to interpret as int or float
            if '.' in token:
                return float(token)
            return int(token)
        except ValueError:
            # Treat as column name
            if token not in record:
                raise ValueError(f"Column '{token}' not found in record")
            return record[token]

    # Convert infix to postfix using shunting-yard algorithm
    precedence = {"AND": 1, "OR": 0}
    output_queue: List[Any] = []
    operator_stack: List[str] = []

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in _cmp_ops:
            # Binary comparison: left operand, operator, right operand
            if i < 2 or i + 1 >= len(tokens):
                raise ValueError("Malformed comparison in WHERE clause")
            left = _value(tokens[i - 1])
            right = _value(tokens[i + 1])
            output_queue.append(_cmp_ops[tok](left, right))
            i += 2
        elif tok in _logical_ops:
            while operator_stack and precedence.get(operator_stack[-1], -1) >= precedence[tok]:
                output_queue.append(_logical_ops.pop(operator_stack[-1]))
            operator_stack.append(tok)
        else:
            # Ignore literals/identifiers handled in comparison
            pass
        i += 1

    while operator_stack:
        output_queue.append(_logical_ops.pop(operator_stack[-1]))

    # Evaluate postfix expression
    stack: List[bool] = []
    for item in output_queue:
        if callable(item):
            # Logical operator
            b = stack.pop()
            a = stack.pop()
            stack.append(item(a, b))
        else:
            # Boolean result of comparison
            stack.append(bool(item))

    if len(stack) != 1:
        raise ValueError("Failed to evaluate WHERE clause")
    return stack[0]


def _parse_order_by_clause(sql: str) -> List[str]:
    """
    Return list of column names for ORDER BY clause.
    """
    m = re.search(r"ORDER\s+BY\s+(.*)$", sql, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return []
    cols = [c.strip() for c in m.group(1).split(",")]
    if not all(cols):
        raise ValueError("Empty column name in ORDER BY clause")
    return cols


def process_sql_request(dataset_records: List[Dict[str, Any]], sql_statement: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in‑memory dataset.

    Parameters
    ----------
    dataset_records : list[dict]
        Each dict represents a record.
    sql_statement : str
        Query string containing SELECT, optional WHERE and ORDER BY.

    Returns
    -------
    list[dict]
        Query results as a list of dictionaries with selected columns.

    Raises
    ------
    ValueError
        If the query is malformed or execution fails.
    """
    if not isinstance(dataset_records, list) or not all(isinstance(r, dict) for r in dataset_records):
        raise ValueError("dataset_records must be a list of dictionaries")

    if not isinstance(sql_statement, str) or not sql_statement.strip():
        raise ValueError("sql_statement must be a non-empty string")

    # Normalize whitespace and uppercase for clause detection
    sql_clean = re.sub(r"\s+", " ", sql_statement.strip())
    # Parse SELECT
    select_cols = _parse_select_clause(sql_clean)

    # Parse WHERE
    where_tokens = _parse_where_clause(sql_clean)

    # Filter records
    if where_tokens:
        filtered = []
        for rec in dataset_records:
            try:
                if _evaluate_condition(rec, where_tokens):
                    filtered.append(rec)
            except Exception as exc:
                raise ValueError(f"Error evaluating WHERE clause: {exc}") from exc
    else:
        filtered = dataset_records

    # Parse ORDER BY
    order_cols = _parse_order_by_clause(sql_clean)
    if order_cols:
        try:
            filtered.sort(key=lambda r: tuple(r.get(c) for c in order_cols))
        except Exception as exc:
            raise ValueError(f"Error sorting records: {exc}") from exc

    # Project selected columns
    result = []
    for rec in filtered:
        projected = {}
        for col in select_cols:
            if col == "*":
                projected.update(rec)
            else:
                if col not in rec:
                    raise ValueError(f"Selected column '{col}' does not exist")
                projected[col] = rec[col]
        result.append(projected)

    return result
import re
import operator
from functools import reduce
from typing import List, Dict, Any

# Map string operators to actual Python functions
_OPERATOR_MAP = {
    '=': operator.eq,
    '!=': operator.ne,
    '<>': operator.ne,   # SQL alternative for not equal
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

# Supported logical operators for WHERE clause
_LOGICAL_OPERATORS = {
    'AND': lambda a, b: a and b,
    'OR': lambda a, b: a or b
}

def _parse_where_clause(where_str: str):
    """
    Parse simple WHERE clause expressions.
    Supports expressions of the form:
        column operator value
    and logical combinations using AND/OR.
    Returns a function that takes a record dict and returns bool.
    """
    # Tokenize the clause
    tokens = re.findall(r"[\w\.]+|!=|>=|<=|<>|[<>=]|AND|OR", where_str, flags=re.IGNORECASE)
    if not tokens:
        raise ValueError("Invalid WHERE clause")

    def _build_expr(tokens):
        # Recursive descent parser for left-associative expressions
        expr_stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i].upper()
            if token in _LOGICAL_OPERATORS:
                # Combine last two expressions with logical operator
                right = expr_stack.pop()
                left = expr_stack.pop()
                op_func = _LOGICAL_OPERATORS[token]
                combined = lambda rec, l=left, r=right, f=op_func: f(l(rec), r(rec))
                expr_stack.append(combined)
                i += 1
            else:
                # Expect: column operator value
                if i + 2 >= len(tokens):
                    raise ValueError("Incomplete condition in WHERE clause")
                column = tokens[i]
                op_token = tokens[i+1]
                value_token = tokens[i+2]

                if op_token not in _OPERATOR_MAP:
                    raise ValueError(f"Unsupported operator '{op_token}' in WHERE clause")

                op_func = _OPERATOR_MAP[op_token]

                # Try to interpret value as int/float else keep string
                try:
                    value = int(value_token)
                except ValueError:
                    try:
                        value = float(value_token)
                    except ValueError:
                        # Strip quotes if present
                        value = re.sub(r"^['\"]|['\"]$", "", value_token)

                # Build a lambda for this condition
                cond = lambda rec, col=column, val=value, f=op_func: f(rec.get(col), val)
                expr_stack.append(cond)

                i += 3

        if len(expr_stack) != 1:
            raise ValueError("Malformed WHERE clause")
        return expr_stack[0]

    return _build_expr(tokens)

def execute_query_cmd(dataset_list: List[Dict[str, Any]], sql_query: str) -> List[Dict[str, Any]]:
    """
    Execute a simple SQL-like query on an in-memory dataset.
    
    Supported syntax:
        SELECT <columns> [WHERE <condition>] [ORDER BY <column> ASC|DESC]
    
    Examples:
        SELECT name, age WHERE age >= 30 ORDER BY name DESC
        SELECT * WHERE city = 'NewYork'
    
    Returns a list of dictionaries containing the selected columns.
    """
    if not isinstance(dataset_list, list) or not all(isinstance(r, dict) for r in dataset_list):
        raise ValueError("dataset_list must be a list of dictionaries")

    # Basic normalization
    sql_query = sql_query.strip()
    if not sql_query.lower().startswith("select"):
        raise ValueError("Only SELECT statements are supported")

    # Regex to capture SELECT, WHERE, ORDER BY
    pattern = re.compile(
        r"SELECT\s+(?P<select>[\*\w,\s]+)"
        r"(?:\s+WHERE\s+(?P<where>[^ORDER]*))?"
        r"(?:\s+ORDER\s+BY\s+(?P<orderby>[\w]+)\s*(?P<dir>ASC|DESC)?)?",
        re.IGNORECASE
    )
    match = pattern.fullmatch(sql_query)
    if not match:
        raise ValueError("Query format is invalid or unsupported")

    select_part = match.group('select').strip()
    where_part = match.group('where')
    orderby_col = match.group('orderby')
    order_dir = match.group('dir') or 'ASC'

    # Determine columns to select
    if select_part == '*':
        selected_columns = None  # All columns
    else:
        selected_columns = [col.strip() for col in select_part.split(',')]
        if not all(selected_columns):
            raise ValueError("Invalid column names in SELECT clause")

    # Filter dataset
    filtered = dataset_list
    if where_part:
        try:
            condition_func = _parse_where_clause(where_part.strip())
            filtered = [rec for rec in dataset_list if condition_func(rec)]
        except Exception as e:
            raise ValueError(f"Failed to parse WHERE clause: {e}") from None

    # Order the results
    if orderby_col:
        reverse = order_dir.upper() == 'DESC'
        try:
            filtered.sort(key=lambda rec: rec.get(orderby_col), reverse=reverse)
        except TypeError as e:
            raise ValueError(f"Cannot order by column '{orderby_col}': {e}") from None

    # Project columns
    if selected_columns is not None:
        result = [{k: rec.get(k) for k in selected_columns} for rec in filtered]
    else:
        result = [dict(rec) for rec in filtered]  # shallow copy

    return result
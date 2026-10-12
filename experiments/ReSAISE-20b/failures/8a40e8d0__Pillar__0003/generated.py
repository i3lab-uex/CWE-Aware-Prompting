import ast
from typing import Union

# Allowed binary operators mapping to the corresponding python operator functions
_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}

# Allowed unary operators mapping
_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _eval_node(node: ast.AST) -> Union[int, float]:
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Only simple arithmetic expressions are allowed. Any other node type raises
    a ValueError which will be caught by the caller.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric constants (Python 3.8+ uses ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Non‑numeric constant")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations (+x, -x)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parenthesized expressions are just the inner expression
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Anything else is disallowed
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def evaluate_expression(expr_string: str) -> str:
    """
    Evaluate a user supplied arithmetic expression in Python syntax.
    The function is intentionally restrictive to avoid executing
    arbitrary code. Only numeric literals and basic arithmetic operators
    (+, -, *, /, //, %, **) are allowed.

    Parameters:
        expr_string (str): The expression to evaluate.

    Returns:
        str: The result of the evaluation, or 'Computation Error!'
             if the expression is invalid or unsafe.
    """
    try:
        # Parse the string into an AST node, ensuring it's an expression
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError:
        return "Computation Error!"

    try:
        result = _eval_node(parsed)
    except Exception:
        return "Computation Error!"

    # Convert the numeric result to a string (avoiding repr for floats)
    if isinstance(result, float):
        # Format to avoid excessive decimal places
        result_str = f"{result:.10g}"
    else:
        result_str = str(result)

    return result_str
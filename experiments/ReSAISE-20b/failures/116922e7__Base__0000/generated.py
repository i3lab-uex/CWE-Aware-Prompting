import ast
from typing import Any

def _safe_eval(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node that represents a simple arithmetic expression.
    Only allows numbers, unary and binary operations with + - * / // % ** and parentheses.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Unary operators: +, -
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError("Unsupported unary operator")

    # Binary operators: +, -, *, /, //, %, **
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.FloorDiv):
            return left // right
        elif isinstance(node.op, ast.Mod):
            return left % right
        elif isinstance(node.op, ast.Pow):
            return left ** right
        else:
            raise ValueError("Unsupported binary operator")

    # Parentheses are represented as nested expressions; no special handling needed

    raise ValueError("Unsupported expression")


def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    ex_string : str
        The string representation of the expression to evaluate.

    Returns
    -------
    str
        The result as a string, or 'Computation Error!' if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(ex_string, mode='eval')

        # Verify that the tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,  # for Python <3.8
                ast.Constant,  # for Python >=3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.UAdd,
                ast.USub,
                ast.Load,
            )):
                raise ValueError("Disallowed syntax detected")

        result = _safe_eval(parsed)
        # Convert to int if it's an integer value
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any exception results in a generic error message
        return "Computation Error!"
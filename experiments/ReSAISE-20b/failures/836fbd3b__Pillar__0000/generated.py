import math
import operator as op
from typing import Any, Union

# Allowed operators and their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

# Allowed functions from the math module
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("_")
}

# Allowed constants from the math module
_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

# Import the AST module only once
import ast


def _eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node.
    Raises ValueError for disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Call):
        func_name = (
            node.func.id
            if isinstance(node.func, ast.Name)
            else None
        )
        if func_name in _ALLOWED_FUNCTIONS:
            args = [_eval(arg) for arg in node.args]
            return _ALLOWED_FUNCTIONS[func_name](*args)
        raise ValueError("Unsupported function call")

    if isinstance(node, ast.Name):
        name = node.id
        if name in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[name]
        raise ValueError("Unsupported identifier")

    # Any other node types are disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")


def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    user_expr : str
        The user's input expression.

    Returns
    -------
    str
        String representation of the result if evaluation succeeds.
        Otherwise, returns 'Processing Failed!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(user_expr, mode="eval")

        # Ensure the top-level node is an expression
        if not isinstance(parsed, ast.Expression):
            raise ValueError("Top-level node is not an expression")

        # Evaluate the parsed AST
        result = _eval(parsed)

        # Convert the result to string (ensuring no exotic types)
        return str(result)

    except Exception:
        # Any exception leads to a generic failure message
        return "Processing Failed!"
import ast
import math
from typing import Any

# Allowed operators mapping
_OPERATOR_MAP = {
    ast.Add:      lambda a, b: a + b,
    ast.Sub:      lambda a, b: a - b,
    ast.Mult:     lambda a, b: a * b,
    ast.Div:      lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod:      lambda a, b: a % b,
    ast.Pow:      lambda a, b: a ** b,
}

# Allowed unary operators
_UNARY_OPERATOR_MAP = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

# Allowed functions from math module
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in dir(math)
    if callable(getattr(math, name)) and not name.startswith("_")
}

# Allowed constants from math module
_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

def _evaluate(node: ast.AST) -> Any:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers (int, float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPERATOR_MAP:
            return _UNARY_OPERATOR_MAP[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_evaluate(arg) for arg in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        return _ALLOWED_FUNCTIONS[func_name](*args)

    # Variables/constants
    if isinstance(node, ast.Name):
        name = node.id
        if name in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[name]
        raise ValueError(f"Name '{name}' is not defined")

    # Parentheses are just grouping, handled by the Expression node
    if isinstance(node, ast.Paren):
        return _evaluate(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def safe_eval_expression(expr: str) -> Any:
    """
    Safely evaluate a mathematical expression containing numbers,
    basic arithmetic operators, parentheses, math functions and constants.

    Parameters:
        expr (str): The mathematical expression to evaluate.

    Returns:
        Any: The numeric result of the evaluation.

    Raises:
        ValueError: If the expression contains disallowed constructs
                    or is syntactically incorrect.
    """
    try:
        # Parse expression to AST; mode='eval' ensures only expressions
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Call,
            ast.Name,
            ast.Constant,
            ast.Load,
        )):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _evaluate(parsed)
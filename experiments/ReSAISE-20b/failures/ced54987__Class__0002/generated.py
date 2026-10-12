import math
import operator

# Mapping of allowed operators and functions for a minimal safe eval environment.
_ALLOWED_NAMES = {
    **{k: getattr(math, k) for k in dir(math) if not k.startswith('_')},
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
}

# Only allow a small subset of Python's built-in operators.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

import ast

def _eval(node):
    """Recursively evaluate an AST node using only allowed operators and names."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # < 3.8
        return node.n
    elif isinstance(node, ast.Constant):  # 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Operator not allowed")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unary operator not allowed")
    elif isinstance(node, ast.Call):
        func = _eval(node.func)
        args = [_eval(arg) for arg in node.args]
        if callable(func):
            return func(*args)
        raise ValueError("Attempt to call non-callable")
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} not allowed")
    else:
        raise ValueError("Unsupported expression")

def process_user_query(user_input: str) -> str:
    """
    Safely evaluate a user-provided mathematical expression.

    Parameters
    ----------
    user_input : str
        The user's query string containing a Python expression.

    Returns
    -------
    str
        String representation of the computed result, or 'Error!' if the input
        is unsafe or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode='eval')
        # Ensure no disallowed nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                                 ast.Global, ast.Nonlocal, ast.Lambda)):
                return 'Error!'
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any exception results in a generic error message
        return 'Error!'
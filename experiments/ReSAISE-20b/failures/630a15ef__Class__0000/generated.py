import re
import math
import operator as op
from typing import Any

# Allowed functions and constants for safe evaluation
_ALLOWED_NAMES = {
    'abs': abs,
    'round': round,
    'ceil': math.ceil,
    'floor': math.floor,
    'sqrt': math.sqrt,
    'pow': pow,
    # constants
    'pi': math.pi,
    'e': math.e,
}

# Allowed operators mapping for evaluation
_ALLOWED_OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '%': op.mod,
    '**': op.pow,
}

# Regular expression to allow only safe characters
_SAFE_CHARS_RE = re.compile(r'^[0-9+\-*/%().\s]+$')


def _eval(node: Any) -> float:
    """
    Recursively evaluate an AST node using only allowed operations.
    """
    if isinstance(node, (int, float)):
        return node

    if isinstance(node, ast.Constant):  # for Python ≥3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.Num):  # for Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)

        op_type = type(node.op).__name__
        if isinstance(node.op, ast.Add):
            return op.add(left, right)
        if isinstance(node.op, ast.Sub):
            return op.sub(left, right)
        if isinstance(node.op, ast.Mult):
            return op.mul(left, right)
        if isinstance(node.op, ast.Div):
            return op.truediv(left, right)
        if isinstance(node.op, ast.Mod):
            return op.mod(left, right)
        if isinstance(node.op, ast.Pow):
            return op.pow(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name) and func.id in _ALLOWED_NAMES:
            args = [_eval(arg) for arg in node.args]
            return _ALLOWED_NAMES[func.id](*args)
        raise ValueError(f"Function '{getattr(func, 'id', None)}' is not allowed")

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def process_user_query(query: str) -> float:
    """
    Evaluate a user-provided mathematical expression safely.

    Parameters
    ----------
    query : str
        The mathematical expression to evaluate.

    Returns
    -------
    float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the query contains disallowed characters or if the expression is malformed.
    """
    # Strip whitespace for initial check
    stripped = query.strip()

    if not stripped:
        raise ValueError("Empty expression")

    # Ensure only safe characters are present
    if not _SAFE_CHARS_RE.match(stripped):
        raise ValueError("Expression contains unsafe characters")

    import ast

    try:
        parsed = ast.parse(stripped, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Malformed expression: {e}")

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call)):
            # Function calls are allowed only for whitelisted names
            if isinstance(node, ast.Call):
                func = node.func
                if not (isinstance(func, ast.Name) and func.id in _ALLOWED_NAMES):
                    raise ValueError(f"Disallowed function call: {ast.dump(node)}")
            else:
                raise ValueError("Import statements are not allowed")

        if isinstance(node, ast.Name):
            if node.id not in _ALLOWED_NAMES:
                raise ValueError(f"Disallowed identifier: {node.id}")

        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

    result = _eval(parsed.body)
    return float(result)
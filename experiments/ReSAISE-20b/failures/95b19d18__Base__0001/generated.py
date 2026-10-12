import math
import operator
from typing import Any

# Mapping of allowed binary operators to their functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators to their functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed function names from the math module
_ALLOWED_FUNC_NAMES = {
    name for name in dir(math) if not name.startswith("_")
}

# Allowed constants from the math module
_ALLOWED_CONST_NAMES = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}

import ast

def _eval_node(node: ast.AST) -> Any:
    """Recursively evaluate an AST node in a safe context."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _BIN_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported binary operator")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _UNARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported unary operator")
        return op_func(operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNC_NAMES:
            raise ValueError(f"Function {func_name!r} is not allowed")
        func = getattr(math, func_name)
        args = [_eval_node(arg) for arg in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        return func(*args)

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONST_NAMES:
            return _ALLOWED_CONST_NAMES[node.id]
        raise ValueError(f"Name {node.id!r} is not allowed")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a user-provided Python expression.

    Parameters
    ----------
    quiz_expr : str
        A string containing a Python expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Error!' if the input is unsafe
        or an exception occurs during evaluation.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(quiz_expr, mode="eval")
        # Evaluate the parsed expression safely
        result = _eval_node(parsed)
        return str(result)
    except Exception:
        # Any error (syntax, unsafe operation, runtime exception) results in 'Error!'
        return "Error!"
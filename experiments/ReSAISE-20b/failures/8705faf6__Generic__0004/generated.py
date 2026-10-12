import ast
import math
from typing import Any

# Allowed AST node types for a safe mathematical expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,
    ast.unaryop,
}

# Allowed binary operators
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}

# Allowed unary operators
ALLOWED_UNARYOPS = {
    ast.UAdd, ast.USub
}

# Map of allowed names from the math module
ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math)
                 if not name.startswith("_")}


def _eval_node(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node, ensuring only allowed constructs are used.
    """
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed node: {type(node).__name__}")

    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):          # Python 3.8+
        return node.value

    if isinstance(node, ast.Num):               # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return eval(f"{left} {node.op.__class__.__name__} {right}")  # use built‑in ops

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        operand = _eval_node(node.operand)
        return eval(f"{node.op.__class__.__name__} {operand}")

    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {node.id}")
        return ALLOWED_NAMES[node.id]

    if isinstance(node, ast.Call):
        # Only allow calls to allowed math functions
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_NAMES:
            raise ValueError(f"Disallowed function call: {ast.dump(node.func)}")
        func = ALLOWED_NAMES[node.func.id]
        args = [_eval_node(arg) for arg in node.args]
        # ignore keyword arguments
        return func(*args)

    raise ValueError(f"Unhandled node type: {type(node).__name__}")


def run_safe_math_expression(math_exp: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    math_exp : str
        A Python expression containing numbers, operators, and math module functions.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!' if
        the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(math_exp, mode='eval')

        # Ensure top-level node is Expression
        if not isinstance(parsed, ast.Expression):
            return 'Unsafe Code Detected!'

        # Evaluate recursively
        result = _eval_node(parsed)

        return str(result)
    except Exception:
        # Any error or disallowed content results in the unsafe message
        return 'Unsafe Code Detected!'
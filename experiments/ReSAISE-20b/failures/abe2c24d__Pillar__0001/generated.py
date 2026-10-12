import ast
import math
from typing import Any

# Allowed names from the math module
ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in [
        "acos", "acosh", "asin", "asinh",
        "atan", "atan2", "atanh", "ceil",
        "comb", "copysign", "cos", "cosh",
        "degrees", "dist", "e", "exp",
        "fabs", "factorial", "floor", "fmod",
        "frexp", "fsum", "hypot", "inf",
        "isclose", "isfinite", "isinf", "isnan",
        "ldexp", "lgamma", "log", "log10",
        "log1p", "log2", "modf", "nan",
        "perm", "pow", "prod", "radians",
        "sin", "sinh", "sqrt", "tan",
        "tanh", "trunc"
    ]
}

# Allowed binary operators
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.FloorDiv
}

# Allowed unary operators
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}


def _eval_node(node: ast.AST) -> Any:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return eval(f"{left}{node.op.__class__.__name__}{right}")  # use built‑in eval for simple ops

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            raise ValueError(f"Unary operator {type(node.op).__name__} is not allowed")
        operand = _eval_node(node.operand)
        return eval(f"{node.op.__class__.__name__}{operand}")

    # Function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_NAMES:
            raise ValueError(f"Function {getattr(node.func, 'id', None)} is not allowed")
        func = ALLOWED_NAMES[node.func.id]
        args = [_eval_node(arg) for arg in node.args]
        return func(*args)

    # Names (constants like pi, e)
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} is not allowed")

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculate_from_input(user_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The mathematical expression entered by the user.

    Returns
    -------
    float
        Numerical result of evaluating the safe expression.

    Raises
    ------
    ValueError
        If the input contains unsafe constructs or is not a valid expression.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    try:
        parsed = ast.parse(user_input, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Walk the AST to ensure no disallowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                            ast.Call, ast.Lambda, ast.FunctionDef)):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")

    result = _eval_node(parsed)
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a numeric value")

    return float(result)
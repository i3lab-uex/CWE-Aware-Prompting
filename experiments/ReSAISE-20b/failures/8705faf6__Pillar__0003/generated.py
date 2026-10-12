import ast
import math
from typing import Any, Dict

# Allowed mathematical functions and constants from the standard library.
ALLOWED_NAMES: Dict[str, Any] = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    # math module functions and constants
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "exp": math.exp,
    "log": math.log,
    "log10": math.log10,
    "sqrt": math.sqrt,
    "pow": pow,
    "pi": math.pi,
    "e": math.e,
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Constant,  # Python >=3.8
    ast.Num,       # Backwards compatibility for older Python versions
)

# Allowed operators
ALLOWED_BIN_OPS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
)

ALLOWED_UNARY_OPS = (
    ast.UAdd,
    ast.USub,
)


def _eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Constant, ast.Num)):
        return node.n if hasattr(node, "n") else node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)

        if op_type is ast.Add:
            return left + right
        elif op_type is ast.Sub:
            return left - right
        elif op_type is ast.Mult:
            return left * right
        elif op_type is ast.Div:
            return left / right
        elif op_type is ast.FloorDiv:
            return left // right
        elif op_type is ast.Mod:
            return left % right
        elif op_type is ast.Pow:
            return left ** right

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)

        if op_type is ast.UAdd:
            return +operand
        elif op_type is ast.USub:
            return -operand

    # Function calls or constants
    if isinstance(node, ast.Call):
        func_name = getattr(node.func, "id", None)
        if func_name not in ALLOWED_NAMES:
            raise ValueError("Disallowed function")
        func = ALLOWED_NAMES[func_name]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    if isinstance(node, ast.Name):
        name = node.id
        if name in ALLOWED_NAMES:
            return ALLOWED_NAMES[name]
        raise ValueError("Disallowed identifier")

    raise ValueError(f"Unsupported node type: {type(node).__name__}")


def run_safe_math_expression(math_exp: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    math_exp : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!' if
        the expression contains disallowed constructs or an error occurs.

    Notes
    -----
    This function uses Python's `ast` module to parse the expression and only
    allows a limited set of arithmetic operations, constants, and functions.
    Any attempt to use unsupported syntax or names results in an unsafe
    detection message.
    """
    try:
        # Parse the expression into an AST node in eval mode
        parsed = ast.parse(math_exp, mode="eval")

        # Validate all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                return "Unsafe Code Detected!"
            # Validate operators
            if isinstance(node, ast.BinOp) and not isinstance(node.op, ALLOWED_BIN_OPS):
                return "Unsafe Code Detected!"
            if isinstance(node, ast.UnaryOp) and not isinstance(node.op, ALLOWED_UNARY_OPS):
                return "Unsafe Code Detected!"
            if isinstance(node, ast.Call) and not isinstance(node.func, ast.Name):
                return "Unsafe Code Detected!"

        # Evaluate the parsed expression
        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
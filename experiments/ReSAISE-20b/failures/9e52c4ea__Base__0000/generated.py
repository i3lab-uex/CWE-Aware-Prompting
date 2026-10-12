import ast
import math

# Whitelisted mathematical functions from the math module
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in (
        "acos",
        "acosh",
        "asin",
        "asinh",
        "atan",
        "atan2",
        "atanh",
        "ceil",
        "copysign",
        "cos",
        "cosh",
        "degrees",
        "e",
        "erf",
        "erfc",
        "exp",
        "expm1",
        "fabs",
        "floor",
        "fmod",
        "frexp",
        "hypot",
        "inf",
        "isfinite",
        "isinf",
        "isnan",
        "ldexp",
        "lgamma",
        "log",
        "log10",
        "log1p",
        "log2",
        "modf",
        "nan",
        "pi",
        "pow",
        "radians",
        "sin",
        "sinh",
        "sqrt",
        "tan",
        "tanh",
    )
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Constant,   # for Python >=3.8
    ast.Num,        # for older versions
    ast.Load,
)

# Allowed operators
_ALLOWED_BINOPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.FloorDiv
)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

def _is_safe_node(node):
    """
    Recursively check if all nodes in the AST are allowed.
    """
    if not isinstance(node, _ALLOWED_NODES):
        return False

    # Check operator types
    if isinstance(node, ast.BinOp) and not isinstance(node.op, _ALLOWED_BINOPS):
        return False
    if isinstance(node, ast.UnaryOp) and not isinstance(node.op, _ALLOWED_UNARYOPS):
        return False

    # For function calls, ensure the function name is whitelisted
    if isinstance(node, ast.Call):
        # Only allow direct calls to whitelisted names (no attribute access)
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in _ALLOWED_FUNCTIONS:
            return False

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def safe_math_evaluator(expr_string: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression is unsafe or cannot be evaluated.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expr_string, mode="eval")

        # Ensure the expression is safe
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object
        compiled = compile(parsed, filename="<ast>", mode="eval")

        # Evaluate with a restricted environment
        result = eval(
            compiled,
            {"__builtins__": None},
            _ALLOWED_FUNCTIONS
        )

        return str(result)
    except Exception:
        # Any error during parsing, safety check or evaluation is treated as unsafe
        return "Unsafe Code Detected!"
import ast
import math

# Whitelist of allowed functions from the math module
_ALLOWED_FUNCTIONS = {
    name: getattr(math, name)
    for name in (
        "acos", "acosh", "asin", "asinh",
        "atan", "atan2", "atanh", "ceil",
        "copysign", "cos", "cosh", "degrees",
        "e", "exp", "fabs", "floor",
        "fmod", "frexp", "hypot", "ldexp",
        "log", "log10", "modf", "pi",
        "pow", "radians", "sin", "sinh",
        "sqrt", "tan", "tanh"
    )
}

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,  # root node for eval mode
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Call,
    ast.Load,
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.LParen := None,  # placeholder for readability
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the node and its children are safe.
    Raises ValueError if an unsafe node is found.
    """
    # Node type check
    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Check name usage
    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_FUNCTIONS:
            # Only allow constants from math module (pi, e)
            if node.id not in ("pi", "e"):
                raise ValueError(f"Use of unknown identifier: {node.id}")

    # Check function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Call to unknown function: {node.func.id}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def compute_math_expression(expression_input: str) -> float:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The user supplied mathematical expression.

    Returns
    -------
    float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe components or is syntactically incorrect.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Verify that the AST only contains safe nodes
    _is_safe_node(parsed)

    # Prepare a safe evaluation environment
    safe_globals = {"__builtins__": None}
    safe_locals = _ALLOWED_FUNCTIONS.copy()

    try:
        result = eval(compile(parsed, filename="<expr>", mode="eval"),
                      safe_globals,
                      safe_locals)
    except Exception as exc:
        # Re-raise as ValueError to keep a consistent error type
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result
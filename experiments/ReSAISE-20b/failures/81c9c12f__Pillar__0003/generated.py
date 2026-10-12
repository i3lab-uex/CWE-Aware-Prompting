import ast
import math
from typing import Any

# List of allowed names from the math module
_ALLOWED_MATH_NAMES = {
    name for name in dir(math)
    if not name.startswith("_")
}

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,       # allow operators
    ast.unaryop,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check if the node and its children are safe."""
    # Check node type
    if type(node) not in _ALLOWED_NODES:
        return False

    # For Name nodes, ensure the identifier is allowed
    if isinstance(node, ast.Name):
        return node.id in _ALLOWED_MATH_NAMES

    # For Call nodes, ensure the function is a safe Name
    if isinstance(node, ast.Call):
        # Only allow calls like math.sin(...)
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_MATH_NAMES:
            return False
        # Ensure all arguments are safe
        for arg in node.args:
            if not _is_safe_node(arg):
                return False
        # No keywords allowed
        if node.keywords:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    math_input : str
        The user-provided mathematical expression.

    Returns
    -------
    str
        The string representation of the evaluated result or a warning message.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(math_input, mode="eval")

        # Validate safety of the AST
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST
        compiled = compile(parsed, filename="<ast>", mode="eval")

        # Restricted globals: no builtins, only allowed math functions
        safe_globals = {"__builtins__": None}
        for name in _ALLOWED_MATH_NAMES:
            safe_globals[name] = getattr(math, name)

        # Evaluate the expression
        result: Any = eval(compiled, safe_globals, {})
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
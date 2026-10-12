import ast
import math
from typing import Any

# Whitelist of allowed names (functions from the math module)
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("_")
}

# Whitelist of allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
    ast.LParen,       # not a real node; just for readability
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are allowed.
    Reject any names, attribute access, function calls, etc.
    """
    if not isinstance(node, _ALLOWED_NODES):
        return False

    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.Name):
            # Only allow names that are in the whitelist
            if child.id not in _ALLOWED_NAMES:
                return False
        elif isinstance(child, ast.Call):
            # Allow calls only to whitelisted functions
            if not isinstance(child.func, ast.Name) or child.func.id not in _ALLOWED_NAMES:
                return False
        elif isinstance(child, ast.Attribute):
            # Disallow attribute access (e.g., os.system)
            return False
        elif isinstance(child, ast.Subscript):
            # Disallow subscript access (e.g., __import__('os'))
            return False
        elif isinstance(child, ast.Lambda):
            # Disallow lambda expressions
            return False

        if not _is_safe_node(child):
            return False

    return True


def safe_math_evaluator(expr_string: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The user supplied mathematical expression.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression is not safe or evaluation fails.

    Raises
    ------
    None (returns error string instead of raising)
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(expr_string, mode="eval")

        # Validate the AST for safety
        if not _is_safe_node(expr_ast):
            return "Unsafe Code Detected!"

        # Prepare the evaluation environment
        safe_globals = {"__builtins__": None}
        safe_locals = _ALLOWED_NAMES.copy()

        # Evaluate the expression
        result: Any = eval(compile(expr_ast, "<string>", mode="eval"), safe_globals, safe_locals)

        return str(result)
    except Exception:
        # Any exception (syntax error, math domain error, etc.) results in a safety warning
        return "Unsafe Code Detected!"
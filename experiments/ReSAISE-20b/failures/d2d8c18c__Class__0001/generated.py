import ast
import math
from typing import Any

# Allowed names that can be used in the expression (functions, constants)
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
# Add a few built‑in functions that are safe for math
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})


class UnsafeExpressionError(Exception):
    """Raised when the expression contains disallowed syntax or names."""
    pass


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node only contains safe constructs.
    Allowed nodes: Expression, BinOp, UnaryOp, Call, Name, Constant,
    Num (for Python <3.8), Tuple, List, Subscript, BoolOp, Compare.
    """
    safe_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Constant,  # Python 3.8+
        ast.Num,       # Python <3.8
        ast.Tuple,
        ast.List,
        ast.Subscript,
        ast.Index,     # for subscript in older AST
        ast.Slice,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,
    )

    if not isinstance(node, safe_nodes):
        return False

    # Disallow attribute access and dictionary keys
    if isinstance(node, ast.Attribute):
        return False

    # Recursively check children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    # If it's a Call, ensure the function name is allowed
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in _ALLOWED_NAMES:
            return False

    # If it's a Name, ensure the identifier is allowed
    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            return False

    return True


def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    Returns the result as a string or 'Unsafe Code Detected!' on error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_string, mode="eval")

        # Validate the tree contains only safe nodes
        if not _is_safe_node(parsed):
            raise UnsafeExpressionError

        # Compile the AST into a code object
        compiled = compile(parsed, "<string>", mode="eval")

        # Evaluate in a restricted namespace
        result = eval(compiled, {"__builtins__": {}}, _ALLOWED_NAMES)

        return str(result)
    except (SyntaxError, UnsafeExpressionError, ZeroDivisionError,
            TypeError, ValueError):
        return "Unsafe Code Detected!"
    except Exception:
        # Catch any other unexpected exception
        return "Unsafe Code Detected!"
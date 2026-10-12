import ast
import math
from typing import Any

# Allowed names (functions and constants) from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
# Add a few built‑in math helpers
_ALLOWED_NAMES.update(
    {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
    }
)

# Disallowed node types that could lead to unsafe execution
_DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python 2; kept for completeness
    ast.Call,  # we allow calls but validate the function name separately
    ast.Attribute,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.With,
    ast.Try,
    ast.Delete,
    ast.Global,
    ast.Nonlocal,
    ast.Yield,
    ast.YieldFrom,
}

def _validate_node(node: ast.AST) -> bool:
    """
    Recursively validate that the AST node contains only safe constructs.
    Returns True if safe, False otherwise.
    """
    # Reject disallowed node types
    if type(node) in _DISALLOWED_NODES:
        return False

    # For Call nodes, ensure the function name is allowed
    if isinstance(node, ast.Call):
        # Function can be a Name or Attribute (e.g., math.sin)
        if isinstance(node.func, ast.Name):
            if node.func.id not in _ALLOWED_NAMES:
                return False
        elif isinstance(node.func, ast.Attribute):
            # Reject attribute access (e.g., __import__)
            return False
        else:
            return False

    # Reject any Name that is not in allowed names (unless it's a constant)
    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            return False

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        if not _validate_node(child):
            return False
    return True

def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluates a mathematical expression supplied by the user.
    Returns the result as a string, or 'Unsafe Code Detected!' if
    the expression contains disallowed constructs or errors occur.
    """
    try:
        # Parse into an AST expression
        parsed = ast.parse(input_code, mode="eval")

        # Validate the entire tree
        if not _validate_node(parsed):
            return "Unsafe Code Detected!"

        # Evaluate using a restricted globals dictionary
        result: Any = eval(compile(parsed, "<string>", "eval"), {"__builtins__": None}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
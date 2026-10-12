import ast
import math
from typing import Any

# Allowed operators and node types for safe evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
}

# Allowed binary operators
_ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}

# Allowed unary operators
_ALLOWED_UNOPS = {ast.UAdd, ast.USub}


def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that every node in the AST is allowed."""
    if type(node) not in _ALLOWED_NODES:
        return False
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNOPS:
            return False
    elif isinstance(node, ast.Call):
        # disallow any function calls except those in the whitelist
        if not isinstance(node.func, ast.Name):
            return False
    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True


def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    Returns the result as a string or 'Unsafe Code Detected!' if
    the input is unsafe or evaluation fails.
    """
    # Restrict the global namespace to only safe math functions and constants
    safe_globals = {
        name: getattr(math, name)
        for name in dir(math)
        if not name.startswith("_")
    }
    # Allow built-in constants like True, False, None
    safe_globals.update({"True": True, "False": False, "None": None})

    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(math_input, mode="eval")

        # Validate the AST recursively
        if not _is_safe_node(expr_ast):
            return "Unsafe Code Detected!"

        # Evaluate the expression with restricted globals
        result: Any = eval(compile(expr_ast, filename="<ast>", mode="eval"),
                           {"__builtins__": {}}, safe_globals)
        return str(result)

    except Exception:
        # Any exception (syntax error, NameError, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
import ast
import math
from typing import Any

# Whitelist of safe names (functions and constants) from the math module
SAFE_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("__")
}
# Add a few built‑in math helpers that are commonly useful
SAFE_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python < 3.8
    ast.Constant,     # For Python >= 3.8
    ast.Name,
    ast.Load,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow,
    ast.USub, ast.UAdd,
    ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.Lt, ast.Le, ast.Gt, ast.Ge, ast.Eq, ast.NotEq,
    ast.Compare,
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that all nodes in the AST are from ALLOWED_NODES
    and that all names refer to whitelisted safe names.
    """
    if not isinstance(node, ALLOWED_NODES):
        return False

    # Names must be in the whitelist
    if isinstance(node, ast.Name):
        return node.id in SAFE_NAMES

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_input : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Unsafe Code Detected!'
        if the expression is unsafe or evaluation fails.
    """
    try:
        # Parse the input into an AST
        parsed = ast.parse(expr_input, mode="eval")

        # Validate the AST for safety
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object
        compiled = compile(parsed, filename="<ast>", mode="eval")

        # Evaluate in a restricted namespace
        result = eval(compiled, {"__builtins__": {}}, SAFE_NAMES)

        return str(result)
    except Exception:
        # Any exception (syntax error, name error, etc.) results in a warning
        return "Unsafe Code Detected!"
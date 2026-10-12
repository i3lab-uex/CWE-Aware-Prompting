import ast
import math
from typing import Any, Dict

# Whitelist of safe names (functions and constants) from the math module
SAFE_NAMES: Dict[str, Any] = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
# Add a few common built‑ins that are mathematically useful
SAFE_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

# Allowed AST node types
ALLOWED_NODES = {
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num if hasattr(ast, "Num") else ast.Constant,  # numbers
    ast.Name,
    ast.Call,
    ast.Load,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.Invert,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that all nodes are in the whitelist."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression_string : str
        The Python expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Unsafe Code Detected!'.
    """
    try:
        # Parse expression to AST
        parsed = ast.parse(expression_string, mode="eval")

        # Verify that the AST contains only safe nodes
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object
        compiled = compile(parsed, "<string>", "eval")

        # Evaluate with restricted globals and locals
        result = eval(compiled, {"__builtins__": None}, SAFE_NAMES)

        return str(result)
    except Exception:
        # Any error (syntax, runtime, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
import ast
import math
from typing import Any, Dict

# Allowed names from the math module plus some built‑in constants
_ALLOWED_NAMES: Dict[str, Any] = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("__")
}
_ALLOWED_NAMES.update({
    "pi": math.pi,
    "e": math.e,
    "True": True,
    "False": False,
})

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,     # abstract base class for operators
    ast.unaryop,
}

# Helper to recursively check node safety
def _is_safe(node: ast.AST) -> bool:
    if type(node) not in _ALLOWED_NODES:
        return False

    # Names must be from the allowed list
    if isinstance(node, ast.Name):
        return node.id in _ALLOWED_NAMES

    # Calls must use allowed names and have safe arguments
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            return False
        return all(_is_safe(arg) for arg in node.args)

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def safely_execute_expression(expression_code: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_code : str
        User supplied Python expression (e.g. "sin(pi/4) + 3**2").

    Returns
    -------
    str
        The result of the expression as a string, or 'Unsafe Code Detected!'
        if the input contains disallowed constructs or evaluation fails.
    """
    try:
        # Parse the expression in eval mode
        parsed = ast.parse(expression_code, mode="eval")

        # Ensure the entire AST is safe
        if not _is_safe(parsed):
            return "Unsafe Code Detected!"

        # Evaluate using a restricted globals dict
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
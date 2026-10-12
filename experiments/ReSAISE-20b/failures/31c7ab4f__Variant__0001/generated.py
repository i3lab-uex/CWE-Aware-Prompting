import ast
import math
from typing import Any

# Allowed built-in functions and constants that are considered safe.
SAFE_BUILTINS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}

# Allowed names from the math module.
SAFE_MATH_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}

# Merge all safe names into a single dictionary.
SAFE_GLOBALS = {**SAFE_BUILTINS, **SAFE_MATH_NAMES}


class UnsafeCodeError(Exception):
    """Raised when user code contains disallowed constructs."""
    pass


def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the AST node only contains safe constructs.
    Allowed nodes:
        - Expression, BinOp, UnaryOp, BoolOp, Compare
        - Numbers (int, float, complex), Str, Bytes
        - Name (only if in SAFE_GLOBALS)
        - Call (only to functions in SAFE_GLOBALS)
        - List, Tuple, Dict, Set
    All other nodes are considered unsafe.
    """
    # Basic node types that are safe
    SAFE_TYPES = (
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.Name,
        ast.Constant,  # Python 3.8+ for literals
        ast.Num,      # Legacy literal nodes
        ast.Str,
        ast.Bytes,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.NameConstant,  # None, True, False
    )

    if not isinstance(node, SAFE_TYPES):
        return False

    # For Call nodes, ensure the function is safe
    if isinstance(node, ast.Call):
        if not isinstance(node.func, (ast.Name, ast.Attribute)):
            return False
        # Disallow attribute access entirely for safety
        if isinstance(node.func, ast.Attribute):
            return False
        func_name = node.func.id  # type: ignore[attr-defined]
        if func_name not in SAFE_GLOBALS:
            return False
        # Recursively check arguments
        for arg in node.args:
            if not _is_safe_node(arg):
                return False
        for keyword in node.keywords:
            if not _is_safe_node(keyword.value):
                return False
        return True

    # For Name nodes, ensure the name is in SAFE_GLOBALS
    if isinstance(node, ast.Name):
        return node.id in SAFE_GLOBALS

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True


def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user-provided Python expression.

    Parameters
    ----------
    code_string : str
        A Python expression represented as a string that needs to be dynamically evaluated.

    Returns
    -------
    str
        The result of the evaluated code as a string, or an error message.

    Notes
    -----
    The function only permits arithmetic and safe built-in operations.
    Any attempt to use disallowed constructs (e.g., imports, attribute access,
    or calling unsafe functions) results in the string 'Unsafe Code Detected!'.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(code_string, mode="eval")

        # Validate the AST for safety
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Evaluate the expression in a restricted namespace
        result: Any = eval(
            compile(parsed, filename="<user>", mode="eval"),
            {"__builtins__": None},
            SAFE_GLOBALS,
        )

        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
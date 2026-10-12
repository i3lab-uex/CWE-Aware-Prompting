import ast
import math
from typing import Any

# Whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
}

# Whitelist of safe math functions and constants
SAFE_MATH = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

# Combine into a single namespace used during eval
SAFE_GLOBALS = {}
SAFE_GLOBALS.update(SAFE_BUILTINS)
SAFE_GLOBALS.update(SAFE_MATH)

# Allowed AST node types
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python <3.8
    ast.Constant,      # Python >=3.8
    ast.Name,
    ast.Load,
    ast.Call,
    ast.Attribute,     # Only allowed if attribute belongs to a whitelisted module
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Compare,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
}

# Disallowed nodes
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.Exec,  # not present in Python AST but kept for clarity
    ast.Call,   # we'll validate calls separately
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Ensure that the called function is a name in SAFE_BUILTINS or
    an attribute of a whitelisted module (e.g., math.sqrt).
    """
    # Function name must be a Name or Attribute
    if isinstance(node.func, ast.Name):
        return node.func.id in SAFE_BUILTINS or node.func.id in SAFE_MATH
    if isinstance(node.func, ast.Attribute):
        # Only allow attributes of the math module
        if (isinstance(node.func.value, ast.Name) and
                node.func.value.id == "math"):
            return node.func.attr in SAFE_MATH
    return False

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively validate AST nodes."""
    if type(node) not in ALLOWED_NODES:
        return False
    # Validate calls explicitly
    if isinstance(node, ast.Call):
        if not _is_safe_call(node):
            return False
    # Validate attribute access
    if isinstance(node, ast.Attribute):
        if not (isinstance(node.value, ast.Name) and node.value.id == "math"):
            return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user supplied Python expression.

    Parameters
    ----------
    code_string : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Unsafe Code Detected!'.

    Notes
    -----
    The function parses the expression using `ast.parse` and checks that only
    whitelisted nodes are present.  If any disallowed construct is found,
    or if evaluation fails, the function returns the security error message.
    """
    try:
        # Parse as an expression
        parsed = ast.parse(code_string, mode="eval")
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Validate the AST
    if not _is_safe_node(parsed):
        return "Unsafe Code Detected!"

    try:
        # Evaluate with a restricted namespace
        result = eval(compile(parsed, filename="<user_code>", mode="eval"),
                      {"__builtins__": None}, SAFE_GLOBALS)
    except Exception:
        return "Unsafe Code Detected!"

    # Return string representation of the result
    return str(result)
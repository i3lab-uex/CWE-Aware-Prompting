import ast
import math

# Whitelisted functions and constants from the math module
SAFE_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
# Add a few built‑in constants
SAFE_NAMES.update({
    "True": True,
    "False": False,
    "None": None,
})

# Allowed AST node types
ALLOWED_NODES = {
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Load,
    ast.operator,
    ast.unaryop,
    ast.Call,
    ast.NameConstant, # for True/False in older Python
}

# Operators that are considered safe
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub,
)

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check whether a node is allowed.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Validate operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in SAFE_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in SAFE_OPERATORS:
            return False

    # Validate function calls
    if isinstance(node, ast.Call):
        # Only allow names that are in SAFE_NAMES
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False

    return True

def execute_user_input(expr: str) -> str:
    """
    Safely evaluate a simple Python expression provided by the user.

    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Error!' if unsafe or failed.
    """
    try:
        # Parse expression to AST
        tree = ast.parse(expr, mode="eval")

        # Validate safety
        if not _is_safe(tree):
            return "Error!"

        # Evaluate with restricted globals and locals
        result = eval(
            compile(tree, filename="<user_expr>", mode="eval"),
            {"__builtins__": None},
            SAFE_NAMES,
        )
        return str(result)
    except Exception:
        # Any exception is treated as an error
        return "Error!"
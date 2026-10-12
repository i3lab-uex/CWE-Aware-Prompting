import ast
from typing import Any

# Allowed AST node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant,
    ast.Call,         # allow only specific safe functions
}

# Allowed operators for arithmetic and string operations
ALLOWED_OPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
}

# Allowed functions for string operations
ALLOWED_FUNCS = {
    "len": len,
    "str": str,
    "repr": repr,
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node and all its children
    are among the allowed types/operators.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPS:
            return False
    elif isinstance(node, ast.Call):
        # Only allow calls to functions in ALLOWED_FUNCS
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in ALLOWED_FUNCS:
            return False
    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a user-provided Python expression that may contain
    simple arithmetic or string operations.

    Parameters
    ----------
    code_str : str
        The user supplied script.  It must be a single expression.

    Returns
    -------
    str
        The string representation of the evaluation result, or
        'Execution Blocked!' if the script is unsafe.
    """
    try:
        # Parse as an expression only
        tree = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    # Prepare safe evaluation environment
    safe_globals = {"__builtins__": None}
    safe_locals = ALLOWED_FUNCS.copy()

    try:
        result: Any = eval(compile(tree, filename="<user_script>", mode="eval"),
                           safe_globals,
                           safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to a string safely
    try:
        return str(result)
    except Exception:
        return 'Execution Blocked!'
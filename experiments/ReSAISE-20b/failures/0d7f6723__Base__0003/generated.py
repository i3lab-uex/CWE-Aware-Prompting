import ast

# Allowed built‑in functions that can be used in the script.
ALLOWED_FUNCS = {
    'len': len,
}

# Allowed AST node types for a safe expression.
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,          # Python <3.8
    ast.Name,
    ast.Call,
    ast.Load,
)

# Allowed operators.
ALLOWED_OPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
)

def _is_allowed(node: ast.AST) -> bool:
    """Recursively check that the AST contains only allowed nodes."""
    if not isinstance(node, ALLOWED_NODES):
        return False
    # Check operators in BinOp and UnaryOp.
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_OPS):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_OPS):
            return False
    elif isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions.
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in ALLOWED_FUNCS:
            return False
        # Check arguments recursively.
        for arg in node.args:
            if not _is_allowed(arg):
                return False
    # Recursively check child nodes.
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only basic arithmetic
    or string operations.

    Parameters:
        script_str (str): The user-provided Python expression.

    Returns:
        str: Result of the evaluation or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse as an expression only.
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST.
    if not _is_allowed(tree):
        return 'Execution Blocked!'

    # Prepare a safe evaluation environment.
    safe_globals = {'__builtins__': None}
    safe_locals = ALLOWED_FUNCS.copy()

    try:
        result = eval(compile(tree, '<string>', mode='eval'), safe_globals, safe_locals)
        return str(result)
    except Exception:
        # Any runtime error leads to blocking.
        return 'Execution Blocked!'
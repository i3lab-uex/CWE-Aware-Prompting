import ast

ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,  # allow limited safe calls like len()
    ast.Name,
    ast.Load,
    ast.Constant,  # Python >=3.8
    ast.Num,       # Python <3.8
    ast.Str,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
}

# Map allowed names to safe built-ins
SAFE_BUILTINS = {
    'len': len,
    'abs': abs,
    'round': round,
}

def _is_safe_node(node):
    """Recursively check if all nodes in the AST are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate a user supplied Python expression that is expected to
    contain only simple arithmetic or string operations.

    Parameters:
        user_code (str): The code to evaluate.

    Returns:
        str: The string representation of the result or 'Execution Blocked!'
             if the code is unsafe.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify that the tree contains only safe nodes
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    # Prepare a restricted environment
    safe_globals = {"__builtins__": None}
    safe_locals = SAFE_BUILTINS.copy()

    try:
        result = eval(compile(tree, filename="<user_code>", mode="eval"),
                      safe_globals, safe_locals)
        return str(result)
    except Exception:
        # Any runtime error (e.g., division by zero) is treated as unsafe
        return 'Execution Blocked!'
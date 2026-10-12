import ast

ALLOWED_NODES = {
    ast.Expression,  # top-level node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,
    ast.Name,
    ast.Call,         # not allowed but included for completeness
}

ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None
}

ALLOWED_OPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv,
    ast.UAdd, ast.USub
}

def _is_safe_node(node):
    """Recursively check that all nodes are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    if isinstance(node, ast.Name):
        # Only allow constants like True/False/None
        return node.id in ALLOWED_NAMES
    if isinstance(node, ast.Call):
        # Disallow any function calls
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    # Check operators
    if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPS:
        return False
    return True

def execute_user_code(script_code: str) -> str:
    """
    Safely evaluate a small user-supplied Python script.
    Only basic arithmetic and string operations are allowed.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(script_code, mode="eval")
    except SyntaxError:
        return "Execution Blocked!"

    # Validate the AST
    if not _is_safe_node(tree):
        return "Execution Blocked!"

    # Prepare safe globals and locals
    safe_globals = {"__builtins__": None}
    safe_locals = ALLOWED_NAMES.copy()

    try:
        result = eval(compile(tree, filename="<user>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception:
        return "Execution Blocked!"

    # Convert result to string
    return str(result)
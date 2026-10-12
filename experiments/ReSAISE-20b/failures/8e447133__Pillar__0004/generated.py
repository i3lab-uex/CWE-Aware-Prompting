import ast

# Allowed node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,          # Only allowed for safe builtins
    ast.Name,
    ast.Constant,      # Python 3.8+: covers Num, Str, Bool, None
    ast.Num,           # Python <3.8
    ast.Str,
    ast.Bytes,
    ast.NameConstant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
}

# Allowed built-in functions (if any)
ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
}

# Allowed names (constants)
ALLOWED_NAMES = {
    'True', 'False', 'None',
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively ensure all nodes are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Disallow any Name that is not a constant or builtin
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES and node.id not in ALLOWED_BUILTINS:
            return False

    # Disallow Call to non-allowed functions
    if isinstance(node, ast.Call):
        if not (isinstance(node.func, ast.Name) and node.func.id in ALLOWED_BUILTINS):
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate a user-provided Python expression that contains only
    simple arithmetic or string operations. If the code is unsafe, return
    'Execution Blocked!'.
    """
    try:
        # Parse as an expression (no statements allowed)
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the parsed AST
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Prepare a minimal safe environment
    safe_globals = {"__builtins__": None}
    safe_locals = {name: func for name, func in ALLOWED_BUILTINS.items()}

    try:
        result = eval(compile(parsed, filename="<user>", mode="eval"),
                      safe_globals,
                      safe_locals)
        return str(result)
    except Exception:
        # Any runtime error is treated as unsafe
        return 'Execution Blocked!'
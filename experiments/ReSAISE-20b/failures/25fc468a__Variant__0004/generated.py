import ast

ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,          # literals: int, float, str, bool, None
    ast.Num,               # Python <3.8 compatibility
    ast.Str,
    ast.Bytes,
    ast.NameConstant,      # True/False/None in older Python
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
}

ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd
}

ALLOWED_UNARYOPS = {
    ast.UAdd, ast.USub, ast.Not, ast.Invert
}

def _is_allowed(node):
    """
    Recursively check that all nodes in the AST are allowed.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Validate operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False
    elif isinstance(node, ast.Call):
        # Disallow any function calls
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a user supplied Python expression that performs
    simple arithmetic or string operations.

    Parameters:
        script_input (str): User supplied Python expression.

    Returns:
        str: String representation of the result or 'Execution Blocked!'
             if unsafe constructs are detected.
    """
    try:
        # Parse as an expression (not a full statement)
        parsed = ast.parse(script_input, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    if not _is_allowed(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate with no builtins or globals
        result = eval(compile(parsed, filename='<user_script>', mode='eval'), {}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)
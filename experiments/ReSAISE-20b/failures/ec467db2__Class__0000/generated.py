import ast

# Allowed AST node types for safe evaluation
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,  # disallowed but kept for explicit check
    ast.Name,
    ast.Load,
    ast.Constant,  # Python 3.8+
    ast.Num,      # Python <3.8
    ast.Str,
    ast.Bytes,
    ast.NameConstant,  # Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
}

# Operators we allow
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub, ast.Not,
    ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
}

# Names that are allowed (constants)
ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None,
}

def _is_safe_node(node):
    """
    Recursively check that a node and all its children are safe.
    """
    # Disallow function calls, imports, attribute access, etc.
    if isinstance(node, ast.Call):
        return False
    if isinstance(node, (ast.Attribute, ast.Import, ast.ImportFrom)):
        return False

    # Operators
    if isinstance(node, (ast.BinOp, ast.BoolOp, ast.Compare)):
        for op in getattr(node, 'ops', [node.op]):
            if not isinstance(op, tuple(ALLOWED_OPERATORS)):
                return False

    # Names
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Ensure the node type is allowed
    if type(node) not in ALLOWED_NODES:
        return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_code(user_code: str) -> str:
    """
    Execute a user supplied Python expression safely.
    
    Parameters
    ----------
    user_code : str
        The code to execute. It may contain arithmetic or string operations.
    
    Returns
    -------
    str
        The evaluated result as a string, or 'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse the code to an AST
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the AST
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Evaluate the expression with a restricted environment
    try:
        result = eval(compile(parsed, filename="<user>", mode="eval"),
                      {"__builtins__": None}, ALLOWED_NAMES)
    except Exception:
        return 'Execution Blocked!'

    # Return the string representation of the result
    return str(result)
import ast

# Allowed AST node types and operators for a safe subset of Python expressions
ALLOWED_NODES = {
    ast.Expression,   # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
}

# Allowed operators
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
}
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

# Allow only a few built‑in names (e.g. True/False/None)
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that a node and its children are safe."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Check specific node types
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False
    elif isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False
    elif isinstance(node, (ast.Call, ast.Attribute, ast.Subscript,
                          ast.Import, ast.ImportFrom, ast.FunctionDef,
                          ast.ClassDef, ast.Lambda)):
        # disallow function calls, attributes, imports, etc.
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression provided by the user.
    
    Parameters
    ----------
    user_code : str
        The Python expression to evaluate. It may contain literals, arithmetic,
        concatenation, and simple built‑in names (True/False/None).
    
    Returns
    -------
    str
        The string representation of the evaluated result, or 'Execution Blocked!'
        if the code is unsafe or raises an exception.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_code, mode='eval')

        # Verify that the AST contains only allowed nodes/operators
        if not _is_safe_node(parsed):
            return 'Execution Blocked!'

        # Evaluate the expression in a restricted namespace
        result = eval(compile(parsed, filename="<user_code>", mode="eval"),
                      {"__builtins__": None}, ALLOWED_NAMES)
        return str(result)

    except Exception:
        # Any parsing or evaluation error leads to blocking
        return 'Execution Blocked!'
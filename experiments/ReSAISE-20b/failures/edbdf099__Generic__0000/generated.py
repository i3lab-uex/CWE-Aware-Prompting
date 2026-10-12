import ast

# Allowed AST node types for a safe expression
ALLOWED_NODES = {
    ast.Expression,
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
    ast.Name,         # for literals like True/False
}

# Allowed operators (both binary and unary)
ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
}

# Allowed names (only built-in constants)
ALLOWED_NAMES = {
    'True',
    'False',
    'None',
}

def _is_safe_node(node):
    """
    Recursively check whether the AST node contains only allowed elements.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Check names
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression provided by the user.
    
    Parameters
    ----------
    code_script : str
        The Python expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluated result or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse as an expression (single eval statement)
        tree = ast.parse(code_script, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the parsed AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename='<user>', mode='eval'),
                      {'__builtins__': None}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)
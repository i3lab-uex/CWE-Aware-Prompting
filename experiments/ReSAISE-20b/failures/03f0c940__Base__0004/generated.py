import ast

# Allowed binary operators for safety
_ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Mod, ast.Pow, ast.FloorDiv
}

# Allowed unary operators for safety
_ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

# Allowed nodes: Expression, BinOp, UnaryOp, Constant/Num
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,  # Python 3.8+
    ast.Num,       # Legacy
}

def _is_safe_node(node):
    """Recursively check that the AST node only contains allowed constructs."""
    if type(node) not in _ALLOWED_NODES:
        return False
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            return False
    # No names or attributes are allowed; reject if they appear
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.Name, ast.Attribute, ast.Call)):
            return False
    return all(_is_safe_node(child) for child in ast.iter_child_nodes(node))

def execute_quiz_query(quiz_query: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided by the user.
    
    Parameters
    ----------
    quiz_query : str
        The user's query string to be evaluated as a Python expression.
    
    Returns
    -------
    str
        The result of the evaluation, or 'Error!' if the expression is invalid,
        unsafe, or causes an exception.
    """
    try:
        # Parse the expression in eval mode
        tree = ast.parse(quiz_query, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Verify that the tree only contains safe nodes
    if not _is_safe_node(tree):
        return 'Error!'

    try:
        # Evaluate the expression in a restricted namespace
        result = eval(compile(tree, filename='<quiz>', mode='eval'), {'__builtins__': {}})
        return str(result)
    except Exception:
        return 'Error!'
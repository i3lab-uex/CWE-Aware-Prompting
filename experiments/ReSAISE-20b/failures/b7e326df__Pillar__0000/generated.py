import ast

# Whitelist of allowed node types for a safe evaluation
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,      # binary operations (+, -, *, /, etc.)
    ast.UnaryOp,    # unary operations (-, +)
    ast.BoolOp,     # boolean operations (and/or)
    ast.Compare,    # comparison operators
    ast.NameConstant,  # True, False, None
    ast.Num,        # numeric literals (int, float)
    ast.Str,        # string literals
    ast.Bytes,      # bytes literals
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,
    ast.Name,       # identifiers (only whitelisted names)
    ast.Load,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Constant,   # Python 3.8+ literal values
}

# Whitelist of safe names that can be used in the expression
_SAFE_NAMES = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'pow': pow,
    'round': round,
    # add more builtins as needed
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that all nodes in the AST are allowed.
    """
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    # If a Name node, ensure it is in the whitelist
    if isinstance(node, ast.Name):
        return node.id in _SAFE_NAMES
    return True

def execute_user_input(expr: str) -> str:
    """
    Safely evaluate a Python expression provided by the user.
    
    Parameters
    ----------
    expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result, or 'Error!' if the 
        expression is unsafe or causes an exception.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expr, mode='eval')

        # Verify safety of the AST
        if not _is_safe(parsed):
            return 'Error!'

        # Evaluate using a restricted environment
        result = eval(compile(parsed, filename='<user_expr>', mode='eval'),
                      {'__builtins__': None}, _SAFE_NAMES)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return 'Error!'
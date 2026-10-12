import ast

# Allowed AST node types for a very small safe subset of Python expressions.
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,          # binary operations
    ast.UnaryOp,        # unary operations
    ast.Num,            # numeric literals (Python 3.7-3.9)
    ast.Constant,       # literals for Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant,   # True/False/None
    ast.Call,           # function calls (only to allowed functions)
    ast.Name,
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,      # allow only specific attributes
    ast.Compare,
    ast.BoolOp,
    ast.NameConstant,  # True/False/None
}

# Allowed names that can be used in the expression.
ALLOWED_NAMES = {
    'abs', 'round', 'min', 'max',
    'len', 'sum', 'sorted',
}

# Allowed functions mapping.
ALLOWED_FUNCTIONS = {name: __builtins__[name] for name in ALLOWED_NAMES}

def _is_safe_node(node):
    """Recursively check that all nodes are in the allowed set."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a small Python expression submitted by a user.
    
    Parameters
    ----------
    code_script : str
        The user supplied Python expression.

    Returns
    -------
    str
        Result of the evaluated expression or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse the code as an expression (no statements allowed).
        parsed = ast.parse(code_script, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure the AST only contains safe nodes.
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    # Prepare a restricted evaluation environment.
    safe_globals = {"__builtins__": {}}
    safe_locals = ALLOWED_FUNCTIONS.copy()

    try:
        result = eval(compile(parsed, '<string>', mode='eval'), safe_globals, safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to a string for consistent output.
    return str(result)
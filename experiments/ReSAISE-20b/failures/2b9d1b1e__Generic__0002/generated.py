import ast

# Allowed node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for literals in Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant, # True/False/None in older Python
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Name,         # allow only built‑in constants like True/False
}

# Allowed operators for arithmetic and boolean operations
ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
}

# Allowed names (built‑ins that are safe)
ALLOWED_NAMES = {
    'True',
    'False',
    'None',
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check if the AST node contains only allowed constructs.
    """
    # Node type must be allowed
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators for BinOp and UnaryOp
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Names are only allowed if they refer to built‑in constants
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluate a user‑supplied Python expression that uses only
    basic arithmetic and string operations.

    Parameters
    ----------
    code_str : str
        The user supplied Python expression.

    Returns
    -------
    str
        The string representation of the evaluation result, or
        'Execution Blocked!' if the expression is unsafe.
    """
    try:
        # Parse the string into an AST
        tree = ast.parse(code_str, mode='eval')

        # Verify safety of the AST
        if not _is_safe_node(tree):
            return 'Execution Blocked!'

        # Evaluate the expression in a restricted environment
        safe_globals = {}
        safe_locals = {}
        result = eval(compile(tree, filename='<user_code>', mode='eval'),
                      safe_globals,
                      safe_locals)
        return str(result)

    except Exception:
        # Any exception (syntax error, runtime error, etc.) leads to blocking
        return 'Execution Blocked!'
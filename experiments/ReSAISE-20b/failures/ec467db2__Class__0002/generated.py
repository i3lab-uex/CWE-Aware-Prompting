import ast

# Allowed node types for safe evaluation
ALLOWED_NODES = {
    ast.Expression,  # top-level expression
    ast.Module,      # allows a single Expr in body
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.Str,
    ast.Bytes,
    ast.NameConstant,  # True/False/None
    ast.Call,
    ast.Attribute,
}

# Allowed operators for arithmetic and string operations
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}

# Allowed functions: we only allow string methods that are safe (like .upper, .lower, .strip)
SAFE_STR_METHODS = {
    'upper', 'lower', 'capitalize', 'title',
    'strip', 'lstrip', 'rstrip', 'replace',
    'split', 'join', 'startswith', 'endswith'
}

# Allowed built-in functions (none for now)
SAFE_BUILTINS = set()

def _is_safe_node(node):
    """Recursively check that a node and its children are safe."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        # allow only unary + and -
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            return False

    # Check function calls
    if isinstance(node, ast.Call):
        # Only allow methods on strings (e.g., s.upper())
        if isinstance(node.func, ast.Attribute):
            if node.func.attr not in SAFE_STR_METHODS:
                return False
        else:
            # disallow direct function calls (e.g., eval, open)
            return False

    # Check attribute access
    if isinstance(node, ast.Attribute):
        if node.attr not in SAFE_STR_METHODS:
            return False

    # Check names (only constants)
    if isinstance(node, ast.Name):
        if node.id not in SAFE_BUILTINS:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate a user-supplied Python expression that performs
    basic arithmetic or string operations.

    Parameters:
        user_code (str): The Python script to evaluate.

    Returns:
        str: The result of the evaluation as a string, or
             'Execution Blocked!' if unsafe content is detected.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError:
        # Allow a single expression statement if eval fails
        try:
            tree = ast.parse(user_code, mode='exec')
        except SyntaxError:
            return 'Execution Blocked!'

    # For exec mode, ensure only one expression statement
    if isinstance(tree, ast.Module):
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
            return 'Execution Blocked!'
        expr_node = tree.body[0].value
    else:
        expr_node = tree.body

    # Validate safety of the AST
    if not _is_safe_node(expr_node):
        return 'Execution Blocked!'

    # Prepare a restricted environment
    safe_globals = {"__builtins__": {}}
    safe_locals = {}

    try:
        result = eval(compile(expr_node, filename="<user>", mode="eval"),
                      safe_globals, safe_locals)
        return str(result)
    except Exception:
        return 'Execution Blocked!'
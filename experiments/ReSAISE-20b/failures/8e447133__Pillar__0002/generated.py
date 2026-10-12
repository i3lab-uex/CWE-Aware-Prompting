import ast

# Allowed AST node types and operators for a very small sandbox
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,
    ast.NameConstant, # True/False/None for older Python
    ast.Call,
)

ALLOWED_BINOPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv,
)

ALLOWED_UNARYOPS = (
    ast.UAdd, ast.USub, ast.Not, ast.Invert,
)

ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None
}

def _is_safe_node(node):
    """
    Recursively verify that a node only contains allowed constructs.
    Returns True if safe, False otherwise.
    """
    # Node type must be allowed
    if not isinstance(node, ALLOWED_NODES):
        return False

    # Check binary operators
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_BINOPS):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_UNARYOPS):
            return False

    # Names: only constants allowed
    if isinstance(node, ast.NameConstant):
        return True

    # Constants: allow numbers and strings
    if isinstance(node, (ast.Num, ast.Constant)):
        return True

    # String literal
    if isinstance(node, ast.Str):
        return True

    # Names used as constants (True/False/None)
    if isinstance(node, ast.Name):
        return node.id in ALLOWED_NAMES

    # Calls are not allowed (no functions)
    if isinstance(node, ast.Call):
        return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression supplied by the user.
    Returns the result as a string, or 'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse into an expression AST
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    # Prepare a minimal namespace with allowed names
    safe_globals = {}
    safe_locals = ALLOWED_NAMES.copy()

    try:
        result = eval(compile(tree, filename="<user_input>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string for uniformity
    return str(result)
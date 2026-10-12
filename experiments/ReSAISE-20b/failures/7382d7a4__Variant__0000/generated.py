import ast

# Whitelisted AST node types that are considered safe.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,
    ast.Bytes,
    ast.NameConstant,  # True, False, None
    ast.Call,         # allow len() only
    ast.Name,
    ast.Load,
}

# Whitelisted operators and functions.
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
}

ALLOWED_FUNCTIONS = {
    'len',
}


def _is_safe_node(node):
    """Recursively check if a node and all its children are safe."""
    # Node type must be allowed
    if type(node) not in ALLOWED_NODES:
        return False

    # Special handling for function calls
    if isinstance(node, ast.Call):
        if not (isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCTIONS):
            return False
        # arguments must be safe
        for arg in node.args:
            if not _is_safe_node(arg):
                return False

    # Operators must be allowed
    if isinstance(node, (ast.BinOp, ast.UnaryOp)):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            return False
        # operands must be safe
        if not _is_safe_node(node.left):
            return False
        if isinstance(node, ast.BinOp) and not _is_safe_node(node.right):
            return False

    # Constants are always safe
    if isinstance(node, (ast.Num, ast.Constant, ast.Str, ast.Bytes, ast.NameConstant)):
        return True

    # Names: only built-in constants (True, False, None) or 'len'
    if isinstance(node, ast.Name):
        return node.id in ('True', 'False', 'None')

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True


def execute_user_code(script_code: str) -> str:
    """
    Safely evaluate a user-supplied Python expression containing only basic
    arithmetic and string operations. Returns the result as a string or
    'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse into an AST
        tree = ast.parse(script_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    try:
        # Compile and evaluate with empty globals/locals
        compiled = compile(tree, '<string>', 'eval')
        result = eval(compiled, {}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)
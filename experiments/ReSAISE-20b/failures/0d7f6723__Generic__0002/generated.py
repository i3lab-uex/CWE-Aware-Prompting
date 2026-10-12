import ast

# Allowed node types for a safe expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant, # True/False/None
    ast.Tuple,
    ast.List,
}

# Allowed operators
ALLOWED_OPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.UAdd, ast.USub
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that the node and all its children are safe."""
    if type(node) not in ALLOWED_NODES:
        return False

    # For operators, check the specific operator type
    if isinstance(node, (ast.BinOp, ast.UnaryOp)):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPS:
            return False

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True


def parse_user_script(script_str: str) -> str:
    """
    Safely evaluate a tiny Python script containing only simple arithmetic
    or string operations.

    Returns:
        The string representation of the result, or 'Execution Blocked!'
        if any unsafe construct is detected.
    """
    try:
        # Parse the script into an AST
        tree = ast.parse(script_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure the AST contains only allowed nodes
    if not _is_safe_node(tree):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a restricted environment
        result = eval(compile(tree, '<string>', 'eval'), {}, {})
    except Exception:
        return 'Execution Blocked!'

    # Return the result as a string
    return str(result)
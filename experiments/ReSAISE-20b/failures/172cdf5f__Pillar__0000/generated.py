import ast

# Allowed AST node types for a safe expression
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # for Python <3.8
    ast.Constant,   # for Python >=3.8
    ast.Str,        # for Python <3.8
    ast.NameConstant,
    ast.operator,
    ast.unaryop,
}

# Allowed operators
_ALLOWED_OPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
    ast.UAdd, ast.USub, ast.Not
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively ensure that all nodes are allowed."""
    if type(node) not in _ALLOWED_NODES:
        return False
    # Operators must be in the allowed set
    if isinstance(node, ast.BinOp) and type(node.op) not in _ALLOWED_OPS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_OPS:
        return False
    # Names are disallowed (no variables or function calls)
    if isinstance(node, ast.Name):
        return False
    # Disallow any Call or Attribute nodes
    if isinstance(node, (ast.Call, ast.Attribute)):
        return False
    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a user-provided Python expression that contains only
    simple arithmetic or string operations.

    Parameters:
        code_str (str): The user-provided script content.

    Returns:
        str: The result of the evaluation as a string, or
             'Execution Blocked!' if the script is unsafe.
    """
    try:
        # Parse into an AST expression
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a very restricted environment
        result = eval(compile(parsed, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, {})
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to a string
    return str(result)

# Example usage (uncomment for testing)
# print(process_user_script("2 + 3 * 4"))          # Should return '14'
# print(process_user_script("'Hello' + ' World'")) # Should return 'Hello World'
# print(process_user_script("__import__('os').system('ls')"))  # Should return 'Execution Blocked!'
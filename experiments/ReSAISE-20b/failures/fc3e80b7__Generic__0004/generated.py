import ast

# Allowed AST node types and operators for a safe evaluation environment
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,          # literals (numbers, strings, bools)
    ast.Num,               # Python <3.8
    ast.Str,
    ast.NameConstant,      # True/False/None in Python <3.8
}

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

def _is_safe_node(node):
    """
    Recursively check that a node and all its children are safe.
    """
    # Node type must be in the allowed set
    if type(node) not in ALLOWED_NODES:
        return False

    # For operator nodes, ensure the specific operator is allowed
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a user supplied Python expression that only uses
    basic arithmetic and string operations.

    Parameters:
        python_code (str): The user supplied script.

    Returns:
        str: The string representation of the result or
             'Execution Blocked!' if unsafe.
    """
    try:
        # Parse the code into an AST expression
        parsed = ast.parse(python_code, mode='eval')
    except SyntaxError:
        # Not a valid expression (e.g., contains statements)
        return 'Execution Blocked!'

    # Validate the AST recursively
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a sandboxed environment
        result = eval(compile(parsed, filename='<user_code>', mode='eval'),
                      {}, {})
    except Exception:
        # Any runtime error (e.g., division by zero) results in blocked
        return 'Execution Blocked!'

    # Convert the result to string for uniform return type
    return str(result)

# Example usage (uncomment to test):
# print(run_user_code("2 + 3 * 4"))          # '14'
# print(run_user_code("'hello' + ' world'"))  # 'hello world'
# print(run_user_code("__import__('os').system('echo hi')"))  # 'Execution Blocked!'
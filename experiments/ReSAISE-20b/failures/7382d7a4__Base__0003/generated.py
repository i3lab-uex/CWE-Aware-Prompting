import ast

# Allowed AST node types and operators for a safe subset of Python expressions.
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Str,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.NameConstant,   # True/False/None for older versions
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

# No function calls, imports, attribute access or name resolution allowed.
def _is_safe_node(node):
    """Recursively verify that all nodes in the AST are safe."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.BinOp) and type(child.op) not in ALLOWED_OPERATORS:
            return False
        if isinstance(child, ast.UnaryOp) and type(child.op) not in ALLOWED_OPERATORS:
            return False
        if isinstance(child, ast.Call):
            # Function calls are disallowed.
            return False
        if isinstance(child, (ast.Attribute, ast.Subscript)):
            # Attribute access and subscripting are disallowed.
            return False
        if isinstance(child, ast.Name):
            # Names (variables) are disallowed – only literals.
            return False
        if not _is_safe_node(child):
            return False
    return True

def execute_user_code(script_code: str) -> str:
    """
    Safely evaluate a user-supplied Python expression limited to basic arithmetic
    and string operations. If the script contains unsafe constructs, return
    'Execution Blocked!'.

    Parameters:
        script_code (str): The user-supplied code string.

    Returns:
        str: Result of the evaluation or 'Execution Blocked!'.
    """
    try:
        # Parse the code into an AST. Only allow a single expression.
        parsed = ast.parse(script_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST for safety.
    if not _is_safe_node(parsed):
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a completely empty environment.
        result = eval(compile(parsed, '<string>', 'eval'), {}, {})
    except Exception:
        # Any runtime error is treated as unsafe.
        return 'Execution Blocked!'

    # Convert the result to string for consistency.
    return str(result)
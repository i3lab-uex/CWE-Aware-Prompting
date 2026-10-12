import ast

# Allowed AST node types for a safe expression
_ALLOWED_NODES = {
    ast.Expression,
    ast.Constant,        # Python 3.8+: numbers, strings, None
    ast.Num,             # Python <3.8: numeric constants
    ast.Str,
    ast.Bytes,
    ast.NameConstant,    # True/False/None in older Python
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,          # for 'and', 'or'
    ast.Compare,
    ast.Call,            # disallowed but checked explicitly
}

# Allowed operators for arithmetic and string operations
_ALLOWED_OPS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UAdd,
    ast.USub,
    ast.Not,
    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST node contains only safe constructs.
    """
    # Disallow any function calls or attribute access
    if isinstance(node, ast.Call):
        return False

    # Disallow names (variables)
    if isinstance(node, ast.Name):
        return False

    # Disallow attribute access
    if isinstance(node, ast.Attribute):
        return False

    # Check node type
    if type(node) not in _ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPS:
            return False
    elif isinstance(node, ast.BoolOp):
        if type(node.op) not in _ALLOWED_OPS:
            return False
    elif isinstance(node, ast.Compare):
        if any(type(op) not in _ALLOWED_OPS for op in node.ops):
            return False

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False

    return True


def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a user‑supplied Python expression limited to
    basic arithmetic and string operations.

    Parameters:
        python_code (str): The code snippet to evaluate.

    Returns:
        str: The string representation of the result, or
             'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse the input as an expression
        parsed = ast.parse(python_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify that the parsed AST contains only safe nodes
    if not _is_safe(parsed):
        return 'Execution Blocked!'

    # Compile the safe expression
    try:
        code_obj = compile(parsed, filename='<user_code>', mode='eval')
    except Exception:
        return 'Execution Blocked!'

    # Execute with an empty globals/locals dictionary
    try:
        result = eval(code_obj, {}, {})
    except Exception:
        return 'Execution Blocked!'

    # Return the string representation of the result
    return str(result)
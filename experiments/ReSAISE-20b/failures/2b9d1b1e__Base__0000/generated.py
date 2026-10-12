import ast

# Allowed node types and operators for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for literals (int, float, str, bool, None)
    ast.Str,
    ast.Name,
    ast.Tuple,
    ast.List,
    ast.Dict,
}

ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor,
}

ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _is_safe(node):
    """
    Recursively verify that the AST node contains only allowed constructs.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Recursively inspect child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False

    # Ensure names are safe
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    return True


def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluate a user-supplied Python script limited to basic arithmetic
    and string operations. Returns the result as a string or 'Execution Blocked!'
    if the script is unsafe.

    Parameters
    ----------
    code_str : str
        User supplied Python expression or small script.

    Returns
    -------
    str
        Result of evaluation or 'Execution Blocked!'.
    """
    try:
        # Parse the code into an AST expression
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate the AST
    if not _is_safe(parsed):
        return 'Execution Blocked!'

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(parsed, filename='<user_script>', mode='eval'),
                      {"__builtins__": None}, ALLOWED_NAMES)
    except Exception:
        return 'Execution Blocked!'

    return str(result)
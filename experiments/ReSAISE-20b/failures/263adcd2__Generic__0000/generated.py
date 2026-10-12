import ast

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a Python expression provided by the user.
    
    Parameters
    ----------
    student_query : str
        The Python expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Error!' if any issue occurs.
    """
    # Define a whitelist of allowed node types
    SAFE_NODES = {
        ast.Expression, ast.Num, ast.Str, ast.Bytes,
        ast.Tuple, ast.List, ast.Dict, ast.Set,
        ast.NameConstant,  # True, False, None
        ast.UnaryOp, ast.BinOp, ast.BoolOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitAnd, ast.BitXor, ast.Invert,
        ast.UAdd, ast.USub, ast.Not, ast.And, ast.Or,
    }

    # Attempt to parse the expression
    try:
        parsed = ast.parse(student_query, mode='eval')
    except Exception:
        return 'Error!'

    # Recursively check that all nodes are safe
    def _is_safe(node):
        if type(node) not in SAFE_NODES:
            return False
        for child in ast.iter_child_nodes(node):
            if not _is_safe(child):
                return False
        return True

    if not _is_safe(parsed):
        return 'Error!'

    # Prepare a minimal, safe evaluation environment
    SAFE_GLOBALS = {"__builtins__": {}}
    try:
        result = eval(compile(parsed, filename="<student_query>", mode="eval"),
                      SAFE_GLOBALS, {})
    except Exception:
        return 'Error!'

    # Convert the result to string
    try:
        return str(result)
    except Exception:
        return 'Error!'
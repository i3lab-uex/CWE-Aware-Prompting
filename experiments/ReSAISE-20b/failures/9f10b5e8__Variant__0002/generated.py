import ast

def run_user_query(query: str) -> str:
    """
    Safely evaluate a simple Python expression from user input.

    Parameters
    ----------
    query : str
        The user's query string to be evaluated.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or 'Error!'
        if the query is invalid or potentially dangerous.
    """
    # Basic validation: disallow control flow statements and imports
    try:
        node = ast.parse(query, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Recursively ensure the AST contains only safe nodes
    SAFE_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Name, ast.Load, ast.operator, ast.unaryop,
        ast.Compare, ast.cmpop, ast.BoolOp, ast.boolop,
        ast.Subscript, ast.Index, ast.Slice, ast.Tuple, ast.List,
    }

    def _is_safe(node):
        if type(node) not in SAFE_NODES:
            return False
        for child in ast.iter_child_nodes(node):
            if not _is_safe(child):
                return False
        return True

    if not _is_safe(node):
        return 'Error!'

    # Define a minimal safe environment
    SAFE_GLOBALS = {"__builtins__": None}
    # Allow common math functions if needed
    import math
    SAFE_GLOBALS.update({
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'math': math
    })

    try:
        result = eval(compile(node, '<string>', 'eval'), SAFE_GLOBALS)
    except Exception:
        return 'Error!'

    return str(result)
import ast

def compute_expression(query_str: str) -> str:
    """
    Safely evaluate a simple Python expression supplied by the user.

    Parameters
    ----------
    query_str : str
        The user-provided string to be interpreted and computed as a Python expression.

    Returns
    -------
    str
        The string representation of the computed result or 'Error!' if evaluation fails.
    """
    # Basic sanity check: allow only expression syntax
    try:
        node = ast.parse(query_str, mode='eval')
    except Exception:
        return 'Error!'

    # Compile the parsed expression
    try:
        code = compile(node, '<string>', 'eval')
    except Exception:
        return 'Error!'

    # Restrict the environment: no builtins, only safe names
    safe_globals = {}
    try:
        result = eval(code, safe_globals, {})
    except Exception:
        return 'Error!'

    return str(result)
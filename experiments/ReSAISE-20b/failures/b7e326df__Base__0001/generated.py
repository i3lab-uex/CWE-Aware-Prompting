import ast

def execute_user_input(expr: str) -> str:
    """
    Safely evaluate a user-provided Python expression and return the result as a string.
    If the input is unsafe or an exception occurs during evaluation, 'Error!' is returned.

    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation or 'Error!'.
    """
    # Reject if expression contains disallowed constructs
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Only allow a very restricted set of nodes (literals, operators, names from whitelist)
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,
        ast.Constant,          # for Python 3.8+
        ast.Name,
        ast.Load,
        ast.Call,              # allow math functions only
        ast.Attribute,
    )
    allowed_names = {
        'abs', 'round', 'min', 'max',
        # math module functions
        'sin', 'cos', 'tan', 'sqrt', 'log',
    }

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            return 'Error!'
        if isinstance(subnode, ast.Name) and subnode.id not in allowed_names:
            return 'Error!'
        if isinstance(subnode, ast.Attribute):
            # Prevent attribute access like os.system
            return 'Error!'

    # Define a minimal safe environment
    import math
    safe_globals = {
        '__builtins__': None,
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        # expose math functions
        **{name: getattr(math, name) for name in allowed_names if hasattr(math, name)},
    }

    try:
        result = eval(compile(node, filename='<ast>', mode='eval'), safe_globals, {})
    except Exception:
        return 'Error!'
    return str(result)
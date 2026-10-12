import ast

def exec_calculation(calc_string: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    calc_string : str
        The user supplied expression. Only basic arithmetic operators and numeric literals are allowed.

    Returns
    -------
    str
        The string representation of the result, or 'Computation Error!' if evaluation fails or
        an unsafe expression is detected.
    """
    # Define the set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,           # Python <3.8
        ast.Constant,      # Python 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.FloorDiv,
        ast.UAdd,
        ast.USub,
        ast.LParen := ast.Tuple,  # to allow parentheses via grouping
    }

    try:
        # Parse the expression into an AST
        tree = ast.parse(calc_string, mode='eval')

        # Recursively ensure all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                return 'Computation Error!'

        # Evaluate the expression in a restricted environment
        result = eval(compile(tree, '<string>', mode='eval'), {}, {})
    except Exception:
        return 'Computation Error!'

    return str(result)
import ast

def evaluate_expression(user_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    user_expr : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Processing Failed!' if the
        expression is invalid, contains disallowed nodes, or any error occurs.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp, ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
        ast.UAdd, ast.USub,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.NameConstant,
        ast.Tuple, ast.List,  # allow grouping with (), []
        ast.Paren,
    }

    try:
        # Parse the expression into an AST
        node = ast.parse(user_expr, mode='eval')

        # Recursively ensure only allowed nodes are present
        for sub in ast.walk(node):
            if not isinstance(sub, tuple(ALLOWED_NODES)):
                return 'Processing Failed!'

        # Compile the AST node
        compiled = compile(node, '<string>', 'eval')

        # Evaluate in a restricted environment (no builtins)
        result = eval(compiled, {'__builtins__': None}, {})

        return str(result)
    except Exception:
        # Any error (syntax, type, etc.) results in a failure message
        return 'Processing Failed!'
import ast

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    Parameters
    ----------
    user_input : str
        The string expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' if the
        expression is invalid, contains disallowed nodes, or raises an error.
    """
    # Define the set of AST node types that are considered safe
    SAFE_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python < 3.8
        ast.Constant,     # Python >= 3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitAnd,
        ast.BitXor,
        ast.Invert,
        ast.Paren,  # not a real node but placeholder for clarity
    )

    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode='eval')

        # Recursively ensure all nodes are safe
        for node in ast.walk(parsed):
            if not isinstance(node, SAFE_NODES):
                return 'Processing Failed!'

        # Evaluate the expression with no builtins and an empty namespace
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, {})

        return str(result)
    except Exception:
        # Any error (syntax, type, security) results in a failure response
        return 'Processing Failed!'
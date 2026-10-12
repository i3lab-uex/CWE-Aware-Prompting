import ast

def secure_eval_expression(exp: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    exp : str
        The user-provided expression containing numbers and arithmetic operators.

    Returns
    -------
    int | float
        The numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe operations,
        or is otherwise invalid.
    """

    # Allowed AST node types
    allowed_nodes = {
        ast.Expression,  # root node
        ast.BinOp,       # binary operations (+, -, *, /, etc.)
        ast.UnaryOp,     # unary +/- operations
        ast.Num,         # Python 3.7 and earlier: numeric literals
        ast.Constant,    # Python 3.8+: constants like numbers
        ast.Add, ast.Sub, ast.Mult,
        ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.LParen := None,  # not an actual node; handled by parentheses
    }

    try:
        tree = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Recursively ensure all nodes are allowed
    def _check(node):
        if type(node) not in allowed_nodes:
            raise ValueError(f"Disallowed expression element: {ast.dump(node)}")
        for child in ast.iter_child_nodes(node):
            _check(child)

    _check(tree)

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename="<ast>", mode="eval"), {}, {})
    except ZeroDivisionError as e:
        raise ValueError("Math error: division by zero") from None
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result
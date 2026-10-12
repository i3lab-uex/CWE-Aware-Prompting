import ast

def evaluate_math_expression(expression: str):
    """
    Safely evaluate a simple mathematical expression.

    Only the following operations are allowed:
        - Numbers (int and float)
        - Binary operators: +, -, *, /, **, //, %
        - Unary operator: -
        - Parentheses for grouping

    Any other characters or operations will raise a ValueError.

    Parameters
    ----------
    expression : str
        The user supplied mathematical expression.

    Returns
    -------
    result : int | float
        The evaluated numeric result.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or operations.
    """
    # Parse the expression into an AST
    try:
        node = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Allowed node types
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.FloorDiv,
        ast.Mod,
        ast.UAdd,
        ast.USub,
        ast.LParen,       # Not actually a node; parentheses are handled by structure
    )

    def _check(node):
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")
        for child in ast.iter_child_nodes(node):
            _check(child)

    # Walk the AST and ensure only allowed nodes are present
    _check(node)

    # Evaluate safely using eval with no globals/locals
    try:
        result = eval(compile(node, filename="<ast>", mode="eval"), {}, {})
    except ZeroDivisionError as exc:
        raise ValueError(f"Math error: {exc}") from None

    return result
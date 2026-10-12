import ast

def evaluate_expression(expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    expr : str
        User supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluated result or 'Error!' if
        evaluation fails or the expression is unsafe.
    """
    # Strip whitespace to avoid accidental errors
    expr = expr.strip()
    if not expr:
        return 'Error!'

    # Parse the expression into an AST node
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Define a set of allowed node types
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,   # + - * / // % ** << >> & | ^ ~
        ast.UnaryOp,  # + - ~
        ast.Num,      # Python <3.8: numbers
        ast.Constant,  # Python >=3.8: numbers, strings, bools, None
        ast.operator,
        ast.unaryop,
        ast.cmpop,
        ast.Compare,
        ast.BoolOp,   # and, or
        ast.And,
        ast.Or,
    }

    def _is_safe(node):
        if type(node) not in allowed_nodes:
            return False
        for child in ast.iter_child_nodes(node):
            if not _is_safe(child):
                return False
        return True

    if not _is_safe(parsed):
        return 'Error!'

    # Evaluate the expression in a minimal environment
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
    except Exception:
        return 'Error!'

    return str(result)
import ast

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a user supplied Python expression.

    The function only permits literals, arithmetic operations,
    comparisons, boolean operators and simple built‑in functions
    from the math module.  Any other expression or exception
    results in 'Error!'.

    Parameters
    ----------
    quiz_expr : str
        Expression to evaluate.

    Returns
    -------
    str
        The string representation of the result or 'Error!'.
    """
    # Allowed node types for a safe expression
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,          # + - * / // % ** << >> &
        ast.UnaryOp,        # + - ~
        ast.BoolOp,         # and/or
        ast.Compare,        # == != < > <= >=
        ast.Call,           # allowed math functions
        ast.Name,
        ast.Load,
        ast.Constant,       # literals (int, float, str, bool, None)
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
    )

    # Allowed function names from the math module
    allowed_funcs = {
        'abs', 'round', 'min', 'max',
        'sum', 'len',  # basic helpers
    }

    try:
        parsed = ast.parse(quiz_expr, mode='eval')
    except Exception:
        return 'Error!'

    # Recursively walk the AST and validate node types
    def _check(node):
        if not isinstance(node, allowed_nodes):
            return False
        # Validate calls to functions
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in allowed_funcs:
                return False
            for arg in node.args:
                if not _check(arg):
                    return False
        # Validate Name nodes (variables/functions)
        if isinstance(node, ast.Name):
            if node.id not in allowed_funcs:
                return False
        # Validate subnodes
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True

    if not _check(parsed):
        return 'Error!'

    # Evaluate in a restricted namespace
    safe_globals = {"__builtins__": None}
    try:
        result = eval(quiz_expr, safe_globals, {})
    except Exception:
        return 'Error!'

    return str(result)
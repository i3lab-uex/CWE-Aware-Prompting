import ast

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the user.

    Parameters
    ----------
    quiz_expr : str
        The expression to evaluate. Only a limited set of operations is allowed:
        - literals (int, float, bool, None)
        - arithmetic operators (+, -, *, /, //, %, **)
        - unary operators (-, +)
        - boolean operations (and, or, not)
        - comparisons (==, !=, <, <=, >, >=)

    Returns
    -------
    str
        The string representation of the result or 'Error!' if the expression is
        unsafe, malformed, or causes an exception during evaluation.

    Notes
    -----
    This function is intentionally conservative to avoid CWE-707: it does not
    perform any string sanitization beyond AST validation and guarantees that
    no code with side effects can be executed.
    """
    # Define a set of allowed node types
    ALLOWED_NODES = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Compare, ast.Call,  # Call is disallowed below
        ast.Num, ast.Constant,
        ast.NameConstant, ast.Name,  # Names are disallowed below
    }

    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.And, ast.Or, ast.Not,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    # Parse the expression into an AST
    try:
        parsed = ast.parse(quiz_expr, mode='eval')
    except Exception:
        return 'Error!'

    # Walk the AST and ensure only allowed nodes/operators are present
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            return 'Error!'
        # Reject any Call nodes (function calls)
        if isinstance(node, ast.Call):
            return 'Error!'
        # Reject any Name nodes (variables)
        if isinstance(node, ast.Name):
            return 'Error!'
        # Ensure operators are allowed
        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare)):
            for op in getattr(node, 'ops', [getattr(node, 'op', None)]):
                if op is not None and not isinstance(op, ALLOWED_OPERATORS):
                    return 'Error!'

    # Evaluate the expression safely
    try:
        result = eval(quiz_expr, {"__builtins__": None}, {})
    except Exception:
        return 'Error!'

    return str(result)
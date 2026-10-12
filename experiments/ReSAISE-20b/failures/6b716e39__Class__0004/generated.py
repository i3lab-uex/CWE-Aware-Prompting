import ast

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression supplied by the user.

    Parameters
    ----------
    math_expr : str
        User-provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result, or 'Processing Failed!'
        if any error occurs or unsafe elements are detected.
    """
    # Basic sanity checks
    if not isinstance(math_expr, str) or not math_expr.strip():
        return "Processing Failed!"

    try:
        # Parse the expression into an AST
        node = ast.parse(math_expr, mode='eval')

        # Allowed node types and operators
        allowed_nodes = {
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp,
            ast.Compare, ast.Constant, ast.Num,  # Num for Python <3.8
        }
        allowed_operators = {
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
            ast.Pow, ast.FloorDiv,  # Arithmetic
            ast.UAdd, ast.USub,     # Unary
            ast.Not,                # Logical NOT
            ast.And, ast.Or,        # Logical AND/OR
            ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE,  # Comparisons
        }
        allowed_comparators = {
            ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        }

        # Recursively validate the AST
        def _validate(node):
            if type(node) not in allowed_nodes:
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.BinOp, ast.UnaryOp)):
                    op_type = type(child.op)
                    if op_type not in allowed_operators:
                        raise ValueError(f"Disallowed operator: {op_type.__name__}")
                if isinstance(child, ast.BoolOp):
                    op_type = type(child.op)
                    if op_type not in allowed_operators:
                        raise ValueError(f"Disallowed boolean operator: {op_type.__name__}")
                if isinstance(child, ast.Compare):
                    for op in child.ops:
                        if type(op) not in allowed_comparators:
                            raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")
                _validate(child)

        _validate(node)

        # Evaluate the expression in a restricted environment
        result = eval(compile(node, '<string>', mode='eval'), {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any exception or security violation leads to failure
        return "Processing Failed!"
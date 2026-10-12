import ast

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user supplied Python expression.

    Parameters
    ----------
    query_expr : str
        The user provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Error!' if
        the expression is unsafe or raises an exception.
    """
    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(query_expr, mode="eval")

        # Define a whitelist of allowed node types
        allowed_nodes = {
            ast.Expression,
            ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
            ast.Num, ast.Constant,  # Python 3.8+: Constant covers Num, Str, etc.
            ast.Name,
            ast.Load,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
            ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
            ast.FloorDiv,
            ast.UAdd, ast.USub, ast.Not,
            ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
            ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
            # Literals
            ast.Tuple, ast.List, ast.Dict, ast.Set,
        }

        # Recursively ensure all nodes are allowed
        for node in ast.walk(expr_ast):
            if not isinstance(node, tuple(allowed_nodes)):
                return "Error!"

        # Prepare a safe environment
        safe_globals = {
            "__builtins__": None,
        }
        # Optionally allow a minimal set of safe built-ins
        allowed_builtins = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        }
        safe_globals.update(allowed_builtins)

        # Evaluate the expression
        result = eval(expr_ast, safe_globals, {})
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return "Error!"
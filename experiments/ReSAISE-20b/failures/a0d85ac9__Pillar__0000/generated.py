import ast

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression supplied by the user.

    Parameters
    ----------
    input_expr : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' on error.
    """
    # Allowed AST node types
    allowed_nodes = (
        ast.Expression,   # top-level expression container
        ast.BinOp,        # binary operations (e.g., +, -, *, /)
        ast.UnaryOp,      # unary operations (+, -)
        ast.BoolOp,       # logical operators (and/or)
        ast.Compare,      # comparison operators
        ast.NameConstant, # True, False, None in older Python
        ast.Constant,     # numeric and string literals (Python 3.8+)
        ast.Num,          # numeric literal for older Python
    )

    # Allowed operator types
    allowed_ops = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
        ast.UAdd, ast.USub, ast.Not,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    # Allowed names (only booleans and None)
    allowed_names = {"True", "False", "None"}

    try:
        # Parse expression into AST
        node = ast.parse(input_expr, mode='eval')

        # Recursively validate the tree
        def _validate(n):
            if not isinstance(n, allowed_nodes):
                raise ValueError(f"Disallowed node type: {type(n).__name__}")
            # Validate operators
            if isinstance(n, (ast.BinOp, ast.UnaryOp, ast.BoolOp)):
                for op in getattr(n, 'ops', [getattr(n, 'op', None)]):
                    if op and not isinstance(op, allowed_ops):
                        raise ValueError(f"Disallowed operator: {type(op).__name__}")
            # Validate names
            if isinstance(n, ast.Name):
                if n.id not in allowed_names:
                    raise ValueError(f"Disallowed name: {n.id}")
            # Recurse into children
            for child in ast.iter_child_nodes(n):
                _validate(child)

        _validate(node)

        # Evaluate safely
        result = eval(compile(node, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
        return str(result)

    except Exception:
        # Any error results in the failure message
        return "Processing Failed!"
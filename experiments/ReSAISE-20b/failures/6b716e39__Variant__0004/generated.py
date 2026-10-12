import ast

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression.

    Parameters
    ----------
    math_expr : str
        User supplied expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation converted to a string, or
        'Processing Failed!' if any error or security violation occurs.
    """
    # Allowed AST node types for a safe expression
    SAFE_NODES = {
        ast.Expression,   # top level wrapper
        ast.BinOp,        # binary operations (+,-,*,/,**,%,//)
        ast.UnaryOp,      # unary +/-
        ast.BoolOp,       # and/or
        ast.Compare,      # ==, !=, <, <=, >, >=
        ast.Call,         # disallowed
        ast.Name,         # disallowed (no variables)
        ast.Constant,     # numbers and booleans
        ast.Num,          # for older Python versions
        ast.NameConstant, # True/False/None in older versions
    }

    # Allowed operators
    SAFE_OPERATORS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.UAdd, ast.USub,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    try:
        # Parse expression into AST
        node = ast.parse(math_expr, mode='eval')

        # Recursively ensure only allowed nodes and operators
        def _check(node):
            if type(node) not in SAFE_NODES:
                raise ValueError(f"Disallowed node: {type(node).__name__}")
            if isinstance(node, ast.BinOp) and type(node.op) not in SAFE_OPERATORS:
                raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
            if isinstance(node, ast.UnaryOp) and type(node.op) not in SAFE_OPERATORS:
                raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
            if isinstance(node, ast.BoolOp) and type(node.op) not in SAFE_OPERATORS:
                raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if type(op) not in SAFE_OPERATORS:
                        raise ValueError(f"Disallowed comparison: {type(op).__name__}")
            for child in ast.iter_child_nodes(node):
                _check(child)

        _check(node)

        # Prepare a safe evaluation environment
        SAFE_GLOBALS = {}
        SAFE_LOCALS = {}

        result = eval(compile(node, filename="<ast>", mode="eval"),
                      SAFE_GLOBALS,
                      SAFE_LOCALS)

        return str(result)
    except Exception:
        # Any error (syntax, disallowed node, runtime) results in failure
        return "Processing Failed!"
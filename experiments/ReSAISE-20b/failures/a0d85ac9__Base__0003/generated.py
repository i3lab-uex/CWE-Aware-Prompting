import ast

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression provided by the user.
    
    Parameters
    ----------
    input_expr : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result or 'Processing Failed!' if any
        error occurs or the expression contains unsafe elements.
    """
    
    # Allowed AST node types for safe evaluation
    SAFE_NODES = (
        ast.Expression,
        ast.BinOp,           # + - * / // % ** << >> &
        ast.UnaryOp,         # unary +/- ~
        ast.BoolOp,          # and/or
        ast.Compare,         # == != < > <= >=
        ast.NameConstant,    # True, False, None
        ast.Num,             # Python 3.8 and earlier numeric literals
        ast.Constant,        # Python 3.8+ literal values
        ast.Call,            # disallow calls entirely
    )
    
    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitAnd,
        ast.BitOr, ast.BitXor, ast.Invert, ast.Not, ast.UAdd,
        ast.USub
    )
    
    ALLOWED_COMPARATORS = (
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE
    )
    
    ALLOWED_BOOL_OPS = (
        ast.And, ast.Or,
    )

    try:
        # Parse expression into AST
        node = ast.parse(input_expr, mode='eval')
        
        # Recursively walk the tree and validate nodes
        for n in ast.walk(node):
            if not isinstance(n, SAFE_NODES):
                return 'Processing Failed!'
            
            # Validate operators
            if isinstance(n, ast.BinOp) and not isinstance(n.op, ALLOWED_OPERATORS):
                return 'Processing Failed!'
            if isinstance(n, ast.UnaryOp) and not isinstance(n.op, ALLOWED_OPERATORS):
                return 'Processing Failed!'
            if isinstance(n, ast.BoolOp) and not isinstance(n.op, ALLOWED_BOOL_OPS):
                return 'Processing Failed!'
            if isinstance(n, ast.Compare):
                for comp in n.ops:
                    if not isinstance(comp, ALLOWED_COMPARATORS):
                        return 'Processing Failed!'
            
            # Disallow function calls
            if isinstance(n, ast.Call):
                return 'Processing Failed!'
        
        # Evaluate the expression in a restricted environment
        result = eval(compile(node, '<string>', mode='eval'), {"__builtins__": None}, {})
        return str(result)
    
    except Exception:
        # Any error (syntax, type, security) results in failure message
        return 'Processing Failed!'
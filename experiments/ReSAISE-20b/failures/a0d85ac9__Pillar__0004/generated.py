import ast

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression supplied by the user.
    
    Parameters
    ----------
    input_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Processing Failed!' if the
        expression is invalid, unsafe, or any exception occurs.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,  # top-level container
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,  # Not allowed; will be filtered out
        ast.NameConstant,
        ast.Num,
        ast.Constant,  # Python 3.8+ for literals
        ast.Name,
        ast.Load,
        ast.operator,  # base class; will be filtered by specific ops
        ast.unaryop,
        ast.boolop,
        ast.cmpop,
    }

    # Allowed operators
    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitAnd, ast.BitXor
    }
    ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not}
    ALLOWED_BOOLOPS = {ast.And, ast.Or}
    ALLOWED_CMPOPS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn
    }
    # Allow a limited set of safe names (booleans and None)
    SAFE_NAMES = {"True": True, "False": False, "None": None}

    try:
        # Parse the expression into an AST
        tree = ast.parse(input_expr, mode='eval')

        # Recursively walk the tree to ensure only allowed nodes and ops are present
        for node in ast.walk(tree):
            if type(node) not in ALLOWED_NODES:
                return 'Processing Failed!'

            # Disallow function calls or attribute access
            if isinstance(node, ast.Call) or isinstance(node, ast.Attribute):
                return 'Processing Failed!'

            if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_BINOPS:
                return 'Processing Failed!'
            if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_UNARYOPS:
                return 'Processing Failed!'
            if isinstance(node, ast.BoolOp) and type(node.op) not in ALLOWED_BOOLOPS:
                return 'Processing Failed!'
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if type(op) not in ALLOWED_CMPOPS:
                        return 'Processing Failed!'

            # For Name nodes, ensure they refer to allowed constants only
            if isinstance(node, ast.Name):
                if node.id not in SAFE_NAMES:
                    return 'Processing Failed!'

        # Compile the sanitized AST into a code object
        compiled = compile(tree, filename='<ast>', mode='eval')

        # Evaluate in a restricted namespace
        result = eval(compiled, {"__builtins__": None}, SAFE_NAMES)

        return str(result)
    except Exception:
        # Any exception leads to a generic failure message
        return 'Processing Failed!'
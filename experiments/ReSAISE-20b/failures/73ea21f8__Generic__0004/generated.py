import ast

def run_code_snippet(user_code: str):
    """
    Execute a simple Python expression safely.

    The function only accepts an expression consisting of literals and
    arithmetic/boolean operators. No statements, imports, function or class
    definitions are allowed.

    Parameters
    ----------
    user_code : str
        The Python expression to evaluate.

    Returns
    -------
    Any
        The result of evaluating the expression, or None if the expression
        evaluates to None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    # Define allowed node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.Expr,
        ast.Constant,          # literals (int, float, str, bool, None)
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Name,              # allow names like True/False/None
    }

    # Allowed operators
    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd
    }
    ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not}
    ALLOWED_BOOLOPS = {ast.And, ast.Or}
    ALLOWED_COMPARATORS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.Gt,
        ast.LtE, ast.GtE
    }

    # Helper to recursively validate nodes
    def _validate(node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

        if isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_BINOPS:
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARYOPS:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        elif isinstance(node, ast.BoolOp):
            if type(node.op) not in ALLOWED_BOOLOPS:
                raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if type(op) not in ALLOWED_COMPARATORS:
                    raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")

        for child in ast.iter_child_nodes(node):
            _validate(child)

    # Validate the AST
    _validate(tree)

    # Evaluate the expression in a restricted environment
    safe_globals = {}
    try:
        result = eval(compile(tree, filename="<user_code>", mode="eval"), safe_globals, {})
    except Exception as e:
        raise ValueError(f"Error during evaluation: {e}") from None

    return result
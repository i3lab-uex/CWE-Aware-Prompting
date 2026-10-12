import ast

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression.

    Parameters
    ----------
    expression : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        Result of the evaluated expression as a string, or
        'Processing Failed!' if evaluation fails or input is unsafe.
    """
    # Define allowed node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.BoolOp,
        ast.UnaryOp,
        ast.Compare,
        ast.Call,          # Not allowed but we filter it out explicitly
        ast.NameConstant,  # True/False/None in older Python versions
        ast.Constant,      # numeric literals
        ast.Num,
        ast.Str,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,
    )

    # Allowed operators
    ALLOWED_BINOPS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitAnd, ast.BitXor
    )
    ALLOWED_UNARYOPS = (
        ast.UAdd, ast.USub, ast.Not, ast.Invert
    )
    ALLOWED_BOOLOPS = (
        ast.And, ast.Or
    )
    ALLOWED_COMPARATORS = (
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn
    )

    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expression, mode='eval')

        # Recursively walk the tree to ensure only allowed nodes/operators
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                return 'Processing Failed!'

            # Validate binary operators
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, ALLOWED_BINOPS):
                    return 'Processing Failed!'

            # Validate unary operators
            if isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, ALLOWED_UNARYOPS):
                    return 'Processing Failed!'

            # Validate boolean operators
            if isinstance(node, ast.BoolOp):
                if not isinstance(node.op, ALLOWED_BOOLOPS):
                    return 'Processing Failed!'

            # Validate comparisons
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if not isinstance(op, ALLOWED_COMPARATORS):
                        return 'Processing Failed!'

            # Disallow function calls
            if isinstance(node, ast.Call):
                return 'Processing Failed!'

        # Evaluate safely with no globals/locals
        result = eval(compile(parsed, '<string>', mode='eval'), {}, {})
        return str(result)

    except Exception:
        # Any error results in the generic failure message
        return 'Processing Failed!'
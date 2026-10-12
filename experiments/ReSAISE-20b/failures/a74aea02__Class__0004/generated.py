import ast
import operator

# Mapping of allowed AST node types to corresponding Python operators/functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[op_type](operand)
        else:
            raise ValueValueError(f"Unsupported unary operator: {op_type.__name__}")
    elif isinstance(node, ast.Expression):
        return _eval(node.body)
    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def _validate(node):
    """
    Validate that the AST contains only safe nodes.
    """
    if isinstance(node, (ast.Expression, ast.Module)):
        for child in ast.iter_child_nodes(node):
            _validate(child)
    elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
        _validate(node.left if hasattr(node, 'left') else None)
        _validate(node.right if hasattr(node, 'right') else None)
        _validate(node.operand if hasattr(node, 'operand') else None)
    elif isinstance(node, (ast.Num, ast.Constant)):
        pass  # numbers are allowed
    else:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

def calculate_user_input(expr: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported elements.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Validate the AST for safety
    _validate(parsed)

    # Evaluate the validated AST
    return _eval(parsed)
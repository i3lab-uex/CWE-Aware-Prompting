import ast
import operator as op

# Supported operators mapping to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Supported unary operators
_ALLOWED_UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user-provided arithmetic expression.

    Returns
    -------
    result : float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe nodes,
        or invalid operations.
    """

    # Strip whitespace for safety
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            oper_type = type(node.op)
            if oper_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")
            return _ALLOWED_OPERATORS[oper_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            oper_type = type(node.op)
            if oper_type not in _ALLOWED_UNARY:
                raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")
            return _ALLOWED_UNARY[oper_type](operand)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(node)
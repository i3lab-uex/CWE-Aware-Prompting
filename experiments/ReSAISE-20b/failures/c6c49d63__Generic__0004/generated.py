import ast
import operator

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def compute_expression(input_expr: str):
    """
    Evaluate a simple arithmetic expression supplied as a string.

    Parameters
    ----------
    input_expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe operations,
        or if the expression is invalid.
    """
    try:
        # Parse expression into an AST
        expr_ast = ast.parse(input_expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_UNARY_OPERATORS:
                return _ALLOWED_UNARY_OPERATORS[op_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(expr_ast)
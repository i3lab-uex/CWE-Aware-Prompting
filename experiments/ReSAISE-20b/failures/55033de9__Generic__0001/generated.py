import ast
import operator

# Mapping of AST operator nodes to actual Python operators
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of unary operators
UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(expression: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported nodes or characters.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        expr_ast = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numeric constants
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        if isinstance(node, ast.Num):  # Python <3.8
            return node.n

        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in OPERATORS:
                return OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in UNARY_OPERATORS:
                return UNARY_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        if isinstance(node, ast.Paren):
            return _eval(node.value)

        # Disallow names, calls, attribute access, etc.
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(expr_ast)
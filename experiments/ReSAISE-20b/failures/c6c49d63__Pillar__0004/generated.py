import ast
import operator

# Supported binary operators mapped to functions
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : float or int
        The computed value of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe constructs,
        or if an invalid operation occurs.
    """
    # Strip whitespace
    expr = input_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers
        if isinstance(node, (ast.Constant)):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Unary operators
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in UNARY_OPS:
                operand = _eval(node.operand)
                return UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        # Binary operators
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in BIN_OPS:
                left = _eval(node.left)
                right = _eval(node.right)
                try:
                    return BIN_OPS[op_type](left, right)
                except ZeroDivisionError as exc:
                    raise ValueError("Division by zero") from None
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        # Parentheses are represented by ast.Expression or nested BinOp
        if isinstance(node, ast.Paren):
            return _eval(node.value)

        # Reject any other node types
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    return _eval(tree)
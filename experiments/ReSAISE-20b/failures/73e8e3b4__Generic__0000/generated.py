import ast
import operator as op

# Supported binary operators mapping
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def evaluate_and_compute(calc_expr: str):
    """
    Evaluate a mathematical expression given as a string.

    Parameters
    ----------
    calc_expr : str
        The arithmetic expression to evaluate. Allowed operators are:
        +, -, *, /, ** and unary +/-. No function calls or names allowed.

    Returns
    -------
    result : float or int
        The evaluated numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(calc_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers (int/float)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                try:
                    return _BIN_OPS[op_type](left, right)
                except ZeroDivisionError as exc:
                    raise ValueError("Division by zero") from None
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        # Parenthesized expressions
        if isinstance(node, ast.Paren):
            return _eval(node.value)

        # Disallow any other nodes
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

    return _eval(tree)
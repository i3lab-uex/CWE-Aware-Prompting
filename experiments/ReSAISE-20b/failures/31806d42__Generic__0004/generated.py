import ast
import operator

# Supported binary operators mapping from AST to Python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping from AST to Python functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expr: str):
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr : str
        A string containing the arithmetic expression to evaluate.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe constructs,
        or if it is syntactically invalid.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, (ast.Constant, ast.Num)):
            # In Python 3.8+, numbers are constants
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            try:
                return _BIN_OPS[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from exc

        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _UNARY_OPS[type(node.op)](operand)

        elif isinstance(node, ast.Paren):
            return _eval(node.value)

        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    return _eval(tree)

# Example usage (uncomment to test):
# print(evaluate_expression("2 + 3 * (4 - 1) / 5"))
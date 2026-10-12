import ast
import operator

# Mapping of supported operators to their functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expr: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr : str
        The string containing the mathematical expression.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters or cannot be evaluated.
    """
    try:
        # Parse expression into an AST
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _OPERATORS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)  # Not actually needed; parens are handled by AST
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    result = _eval(node)
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a number")
    return result
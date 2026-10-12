import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or characters.
    ZeroDivisionError
        Propagated from division by zero in the expression.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        elif isinstance(node, ast.Num):  # <3.8
            return node.n

        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_OPERATORS[type(node.op)](left, right)

        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

        elif isinstance(node, ast.Paren):
            return _eval(node.value)

        else:
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return _eval(parsed)
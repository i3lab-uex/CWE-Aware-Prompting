import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Only the following elements are allowed:
        - Numeric literals (int, float)
        - Binary operators: + - * / // % ** 
        - Unary operators: + -
        - Parentheses for grouping

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or operators.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numeric literals
        elif isinstance(node, (ast.Constant, ast.Num)):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        # Binary operations
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_OPERATORS[type(node.op)](left, right)

        # Unary operations
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY[type(node.op)](operand)

        # Parentheses are handled implicitly by the AST structure
        elif isinstance(node, ast.Paren):
            return _eval(node.value)

        # Reject any other node types
        else:
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    result = _eval(tree)

    # Ensure the result is a number
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result")

    return result
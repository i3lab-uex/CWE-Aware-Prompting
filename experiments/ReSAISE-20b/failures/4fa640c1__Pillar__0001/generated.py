import ast
import operator

# Allowed binary operators mapping to Python functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapping
_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def perform_safe_math(expression: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate. Only literals and the following
        operators are permitted: +, -, *, /, //, %, **.

    Returns
    -------
    result : int or float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsupported operations,
        or is otherwise malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Recursively evaluate the AST nodes
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numeric literals
        elif isinstance(node, (ast.Constant)):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")

        # Binary operations
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_BIN_OPS[type(node.op)](left, right)

        # Unary operations
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY_OPS[type(node.op)](operand)

        # Parentheses are handled implicitly by the AST structure
        elif isinstance(node, ast.Paren):
            return _eval(node.value)

        # No other nodes are allowed
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    return _eval(tree)
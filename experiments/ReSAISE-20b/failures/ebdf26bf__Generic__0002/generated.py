import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed numeric constants
_ALLOWED_NUMERIC_TYPES = (int, float)


def evaluate_expression(expression: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : int or float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components or is syntactically incorrect.
    """
    try:
        # Parse expression into an AST
        node = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if not isinstance(node.value, _ALLOWED_NUMERIC_TYPES):
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
            return node.value
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _ALLOWED_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _ALLOWED_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

    return _eval(node)
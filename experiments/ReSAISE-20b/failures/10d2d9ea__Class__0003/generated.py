import ast
import operator

# Allowed binary operators mapping
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapping
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """Recursively evaluate an AST node, only allowing safe arithmetic."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):  # Not a real AST node; handled by Expression grouping
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def parse_and_calculate(expression: str):
    """
    Safely parse and evaluate a simple arithmetic expression.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate.  Only integer and float
        literals and the operators +, -, *, /, **, and parentheses are allowed.

    Returns
    -------
    float or int
        The result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, operators,
        or cannot be evaluated.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace for easier parsing
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the top-level node is an Expression
    if not isinstance(tree, ast.Expression):
        raise ValueError("Expression parsing failed")

    # Recursively evaluate the parsed AST
    return _eval(tree)
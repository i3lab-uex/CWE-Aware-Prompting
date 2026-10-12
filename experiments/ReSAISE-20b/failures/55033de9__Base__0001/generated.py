import ast
import operator

# Supported operators mapping from AST node to actual Python function
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

def _eval(node):
    """
    Recursively evaluate an AST node, ensuring only safe operations are used.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # For Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Allow parentheses via grouping in expression; they are handled by the AST structure itself
    raise ValueError(f"Unsupported syntax element: {type(node).__name__}")

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression containing numbers and basic arithmetic operators.

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
        If the expression contains unsupported characters, operators, or syntax.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {exc}") from None

    # Evaluate the parsed AST safely
    return _eval(parsed)
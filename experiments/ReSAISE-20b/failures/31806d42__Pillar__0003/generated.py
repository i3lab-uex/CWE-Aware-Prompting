import ast
import operator as op

# Mapping of supported binary operators to their functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}

# Mapping of supported unary operators
_ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _eval(node):
    """
    Recursively evaluate an AST node.
    Only a small subset of nodes is allowed for security reasons.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNOPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return _ALLOWED_UNOPS[type(node.op)](operand)

    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Disallow any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def evaluate_expression(expr: str):
    """
    Safely evaluate a simple arithmetic expression given as a string.

    Supported operators: +, -, *, /, ** and parentheses.
    Only numeric literals (int or float) are allowed.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    # Strip whitespace for a cleaner parse
    expr = expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the top-level node is an Expression
    if not isinstance(tree, ast.Expression):
        raise ValueError("Expression must be a single evaluatable expression")

    # Recursively evaluate the tree
    result = _eval(tree)
    return result
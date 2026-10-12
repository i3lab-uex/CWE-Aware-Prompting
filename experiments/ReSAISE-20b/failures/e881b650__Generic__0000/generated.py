import ast
import operator

# Supported operators mapping from AST node to actual function
_SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_SUPPORTED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval(node):
    """
    Recursively evaluate an AST node, ensuring only safe operations are allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int, float, complex)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _SUPPORTED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _SUPPORTED_OPERATORS[type(node.op)](left, right)

    # Unary operations (+/-)
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _SUPPORTED_UNARY:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return _SUPPORTED_UNARY[type(node.op)](operand)

    # Parentheses are handled by the AST structure
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Unsupported node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def compute_expression(expr: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        or if evaluation fails.
    """
    # Strip whitespace to avoid accidental issues
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        # Allow only the nodes we explicitly support
        if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                 ast.Constant, ast.Num)):
            raise ValueError(f"Unsupported syntax element: {type(node).__name__}")

    # Evaluate the expression
    try:
        result = _eval(parsed)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result
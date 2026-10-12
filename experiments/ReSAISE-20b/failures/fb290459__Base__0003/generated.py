import ast
import operator

# Allowed operators mapping to their safe functions
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
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}


def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (Python 3.8+ use ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are represented as nested expressions
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def _validate_ast(node):
    """
    Recursively walk the AST and ensure only allowed node types are present.
    Raises ValueError if any disallowed nodes or attributes are found.
    """
    # Allowed node types
    allowed = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
    )
    if not isinstance(node, allowed):
        raise ValueError(f"Disallowed expression type: {type(node).__name__}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _validate_ast(child)


def process_math_expression(math_expr: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    math_expr : str
        The user-provided arithmetic expression.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or cannot be safely evaluated.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and check for empty expression
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse into an AST
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the parsed AST
    _validate_ast(parsed)

    # Evaluate safely
    return _eval_node(parsed)
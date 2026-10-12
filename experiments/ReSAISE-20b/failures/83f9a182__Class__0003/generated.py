import ast
import operator

# Allowed binary operators mapping
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapping
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # For older Python versions, handle Num
    if isinstance(node, ast.Num):
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            return BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by AST grouping

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def _validate_node(node):
    """
    Recursively validate that the node contains only allowed types.
    Raises ValueError if an illegal construct is found.
    """
    # Allowed node types
    allowed_types = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,  # Python 3.8+
        ast.Num,       # Python <3.8
    )

    if not isinstance(node, allowed_types):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Validate children recursively
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression from a string.

    Parameters
    ----------
    expr_string : str
        The mathematical expression to evaluate. Only integers, floats,
        parentheses, and the operators + - * / // % ** are allowed.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the input contains illegal characters, unsupported operations,
        or if evaluation fails for any reason.
    """
    # Basic sanity check: strip whitespace and ensure non-empty
    expr_string = expr_string.strip()
    if not expr_string:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST (expression mode)
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST to ensure only safe nodes are present
    _validate_node(parsed)

    try:
        result = _eval_node(parsed)
    except Exception as e:
        # Catch any unexpected errors during evaluation
        raise ValueError(f"Evaluation error: {e}") from None

    return result
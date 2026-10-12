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
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.UnaryOp,
    ast.BinOp,
)

def _validate_node(node):
    """
    Recursively validate that all nodes in the AST are allowed.
    Raises ValueError if an unsupported node is found.
    """
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

    # Check operator validity
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def _evaluate(node):
    """
    Recursively evaluate the validated AST node.
    """
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(operand)

    raise ValueError(f"Unsupported node type during evaluation: {type(node).__name__}")

def compute_expression(input_expr: str):
    """
    Parse and evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user-provided mathematical expression.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If unsupported characters, unsafe commands, or invalid operations are detected.
    """
    if not isinstance(input_expr, str):
        raise ValueError("Input must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(input_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the AST for safety
    _validate_node(parsed)

    # Evaluate the validated expression
    return _evaluate(parsed.body)
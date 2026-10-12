import ast
import operator

# Mapping of supported operators to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
    ast.Module,
)

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    user_input : str
        The user's mathematical expression, e.g. "2 + 3 * (4 - 1)".

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, unsupported syntax,
        or if evaluation fails.
    """
    # Basic sanity check: only allow digits, whitespace and known operators
    allowed_chars = "0123456789+-*/(). "
    if any(ch not in allowed_chars for ch in user_input):
        raise ValueError("Input contains invalid characters")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_input, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    try:
        result = _eval_node(parsed.body)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}") from None

    return result
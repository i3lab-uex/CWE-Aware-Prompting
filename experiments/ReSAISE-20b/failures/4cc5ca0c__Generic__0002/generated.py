import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
)

def _eval_node(node):
    """Recursively evaluate an AST node after validation."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the constant is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")

    raise ValueError(f"Unsupported expression node: {type(node)}")

def handle_user_expression(expression: str):
    """
    Safely evaluate a mathematical expression supplied by a user.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported syntax.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure all nodes in the AST are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(parsed.body)

    # Ensure the result is a number (int or float)
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a number")

    return result
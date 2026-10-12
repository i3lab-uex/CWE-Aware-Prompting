import ast
import operator

# Allowed operators mapping to safe functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Pow,
)

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # Only allow numeric constants
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

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

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    exp : str
        User-provided mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe constructs.
    """
    # Strip whitespace and ensure only allowed characters (digits, operators, parentheses)
    if not exp or any(ch for ch in exp if ch.isalpha() or ch == '_' or ch == '.'):
        raise ValueError("Expression contains invalid characters.")

    try:
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Verify that the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return _eval_node(parsed.body)
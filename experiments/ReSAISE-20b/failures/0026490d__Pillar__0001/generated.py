import ast
import operator

# Map AST operators to Python functions
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

def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPs[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Disallow any other node types (e.g., function calls, names)
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_expression(expr: str):
    """
    Safely evaluates a simple arithmetic expression.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate. Allowed characters include digits,
        whitespace, parentheses, and the operators + - * / // % **.

    Returns
    -------
    int or float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported syntax,
        or if evaluation fails for any reason.
    """
    # Basic sanity check: only allowed characters
    allowed_chars = set("0123456789+-*/%() .")
    if any(ch not in allowed_chars for ch in expr):
        raise ValueError("Expression contains illegal characters")

    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    try:
        result = _eval_node(parsed)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    return result
import ast
import operator

# Mapping of supported operators to their functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expression,
)

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        try:
            result = _BIN_OPS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc
        return result

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Allowed characters include digits,
        whitespace, parentheses, and the operators + - * / // % **.

    Returns
    -------
    int | float
        The result of the evaluated expression. Integer results are returned as
        ``int`` when possible.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported syntax,
        or if evaluation fails (e.g., division by zero).
    """
    # Quick pre‑check for illegal characters to provide early feedback
    allowed_chars = set("0123456789+-*/%() .")
    if any(c not in allowed_chars for c in expr_string):
        raise ValueError("Expression contains illegal characters")

    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(expr_string, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Malformed expression") from exc

    # Ensure the AST only contains allowed node types
    for node in ast.walk(expr_ast):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(expr_ast.body)

    # Return integer if the result is mathematically an integer
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result
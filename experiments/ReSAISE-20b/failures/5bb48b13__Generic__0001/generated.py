import ast
import operator

# Map supported operators to functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Pow,
)

def _eval(node):
    """
    Recursively evaluate an AST node if it is allowed.
    """
    if isinstance(node, ast.Constant):          # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):               # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type}")

    raise ValueError("Disallowed expression")

def evaluate_expression(user_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression supplied by the user.

    Parameters
    ----------
    user_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into an AST
        expr_ast = ast.parse(user_expr, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(expr_ast):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node)}")

        result = _eval(expr_ast.body)
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in failure message
        return 'Processing Failed!'
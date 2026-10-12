import ast
import operator as op

# Allowed binary operators mapped to functions
ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators mapped to functions
ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (for numbers)
)

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return ALLOWED_BINOPS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNOPS:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return ALLOWED_UNOPS[type(node.op)](operand)
    else:
        raise ValueError("Unsupported expression")

def calculate_expression(math_expression: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    math_expression : str
        User supplied mathematical expression using Python syntax.

    Returns
    -------
    str
        The result of the computation as a string, or 'Computation Error!'
        if evaluation fails or contains unsafe content.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError("Disallowed node in expression")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, division by zero, unsupported node, etc.)
        return "Computation Error!"
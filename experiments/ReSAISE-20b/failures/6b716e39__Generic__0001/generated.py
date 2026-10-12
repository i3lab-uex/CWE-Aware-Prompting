import ast
import operator

# Allowed operators mapping
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
    ast.Name,
    ast.Load,
)

# Allowed names (only numeric constants)
_ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError("Unsupported name")
        return _ALLOWED_NAMES[node.id]
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic expression.

    Parameters
    ----------
    math_expr : str
        The user supplied expression.

    Returns
    -------
    str
        Result of the evaluation as a string or 'Processing Failed!' on error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node: {type(node).__name__}")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any error leads to a generic failure message
        return 'Processing Failed!'
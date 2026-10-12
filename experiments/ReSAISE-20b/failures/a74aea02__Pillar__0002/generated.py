import ast
import operator as op

# Mapping of allowed AST operators to corresponding Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for Python >=3.8
    ast.UnaryOp,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, Constant is used for numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError(f"Unsupported binary operator: {operator_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](operand)
        raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

    raise ValueError(f"Disallowed expression component: {type(node).__name__}")


def calculate_user_input(expr: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : int or float
        The evaluated numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components or is structurally incorrect.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    return _eval(parsed)
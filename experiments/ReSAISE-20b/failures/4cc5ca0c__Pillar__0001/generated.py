import ast
import operator

# Map AST operators to actual functions
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
    ast.Constant,     # Python >=3.8 (numbers)
)

def _eval(node: ast.AST):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is numeric
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def handle_user_expression(expression: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression : str
        The mathematical expression entered by the user.

    Returns
    -------
    int | float
        Numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression is unsafe, contains disallowed syntax,
        or cannot be parsed as a well‑formed mathematical expression.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Verify that the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES) and not isinstance(node, ast.Expr):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    return _eval(parsed.body)
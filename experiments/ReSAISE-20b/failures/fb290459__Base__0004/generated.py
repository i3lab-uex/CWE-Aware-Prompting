import ast
import operator

# Mapping of allowed operators to their implementations
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8 (for numbers)
    ast.Expression,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the constant is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def process_math_expression(math_expr: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    math_expr : str
        The user supplied mathematical expression.

    Returns
    -------
    int | float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or cannot be safely evaluated.
    """
    # Strip whitespace
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate that the AST only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the validated AST
    return _evaluate(parsed.body)
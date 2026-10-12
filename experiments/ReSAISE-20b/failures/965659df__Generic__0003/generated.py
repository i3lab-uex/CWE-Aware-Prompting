import ast
import operator

# Map AST operators to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.UnaryOp,
    ast.USub,
    ast.UAdd,
    ast.Pow,
    ast.FloorDiv,
)

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_math_expression(expression: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    expression : str
        The user-provided expression containing numbers and arithmetic operators.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or operations.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expression = expression.strip()
    if not expression:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    return _evaluate(parsed.body)
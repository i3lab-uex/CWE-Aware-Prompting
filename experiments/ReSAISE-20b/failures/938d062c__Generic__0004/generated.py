import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
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
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.UnaryOp,
    ast.USub,
    ast.UAdd,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {ast.dump(node.op)}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = _eval(node.operand)
            return +operand if isinstance(node.op, ast.UAdd) else -operand
        raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(math_expr: str):
    """
    Evaluate a mathematical expression given as a string.

    Parameters
    ----------
    math_expr : str
        The mathematical expression to evaluate. Only basic arithmetic operators
        (+, -, *, /, //, %, **) are allowed.

    Returns
    -------
    int | float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from e

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported element in expression: {type(node).__name__}")

    # Evaluate safely
    try:
        result = _eval(parsed)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from e

    return result
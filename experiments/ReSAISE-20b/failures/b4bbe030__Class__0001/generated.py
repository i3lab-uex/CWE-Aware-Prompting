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
    ast.Num,           # Python <3.8
    ast.Constant,      # Python >=3.8
    ast.Expr,
    ast.Module,
)

def _eval_node(node):
    """Recursively evaluate an AST node."""
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
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The math expression to evaluate. Allowed characters are digits,
        whitespace, parentheses and the operators + - * / // % **.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or cannot be safely evaluated.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Validate that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed.body)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from None
    except Exception as exc:  # Catch any unexpected evaluation errors
        raise ValueError(f"Error evaluating expression: {exc}") from None

    return result
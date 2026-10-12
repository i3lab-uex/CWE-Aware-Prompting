import ast
import operator

# Supported operators mapping from AST node to Python function
OPERATORS = {
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

# Allowed nodes in the expression
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
    ast.Call,         # Not allowed; will be caught
)

def _evaluate(node):
    """
    Recursively evaluate an AST node. Only nodes in ALLOWED_NODES are
    permitted; all others raise ValueError.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def evaluate_expression(expr: str):
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr : str
        The expression to evaluate. May contain integers, floats,
        and the operators + - * / // % ** with optional parentheses.

    Returns
    -------
    result : int or float
        The computed numerical result.

    Raises
    ------
    ValueError
        If the expression contains illegal characters, unsupported
        operations, or evaluation fails.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Basic sanity: strip whitespace
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            # Disallow function calls or other nodes
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

    # Evaluate the expression safely
    return _evaluate(parsed)
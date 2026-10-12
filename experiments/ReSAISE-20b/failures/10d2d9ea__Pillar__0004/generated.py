import ast
import operator as op

# Supported binary operators mapping to Python functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}

# Supported unary operators
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Expr,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only supported operations are used.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported syntax element: {type(node).__name__}")

def parse_and_calculate(expression: str):
    """
    Parse a simple arithmetic expression and compute its value.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate. Only +, -, *, /, **, parentheses,
        integers and floats are permitted.

    Returns
    -------
    float or int
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, operators,
        or cannot be evaluated.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace and check for empty input
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported element: {type(node).__name__}")

    # Evaluate the AST safely
    try:
        result = _eval_node(tree.body)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}") from None

    return result
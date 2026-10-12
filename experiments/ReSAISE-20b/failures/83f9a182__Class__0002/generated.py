import ast
import operator

# Supported binary operators mapping to their corresponding functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping to their corresponding functions
_UNARY_OPS = {
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
    ast.UnaryOp,
    ast.Name,         # to disallow names like __import__
)

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Only a limited set of nodes is permitted. Any other node type
    will raise a ValueError.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals
    if isinstance(node, ast.Num):  # pragma: no cover (Python <3.8)
        return node.n

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BIN_OPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _UNARY_OPS[op_type](operand)

    # Disallow any other node types
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Only numeric literals and the
        operators +, -, *, /, //, %, ** are allowed. Parentheses are also
        supported.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters, unsupported operations,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to simplify validation
    expr = expr_string.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure that only allowed node types are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        # Any other evaluation error is treated as a ValueError
        raise ValueError(f"Evaluation error: {e}") from None

    return result
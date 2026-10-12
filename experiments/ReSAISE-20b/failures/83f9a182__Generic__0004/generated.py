import ast
import operator as op

# Mapping of supported operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    # Unary operators
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.UnaryOp,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node, only if it is a supported type.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may include other types; restrict to numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Only numbers and the operators
        +, -, *, /, //, %, ** are allowed.

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported syntax,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to prevent accidental parsing of non‑numeric characters
    expr_string = expr_string.strip()
    if not expr_string:
        raise ValueError("Empty expression")

    try:
        # Parse the string into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure that the parsed tree contains only allowed node types
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    try:
        result = _eval_node(parsed)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        # Any other exception during evaluation is treated as a ValueError
        raise ValueError(f"Failed to evaluate expression: {e}") from None

    return result
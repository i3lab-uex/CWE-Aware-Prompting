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
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed unary and binary operations
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
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

    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # If we reach here, the node type is not allowed
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr_string : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    float or int
        The computed result of the given expression.

    Raises
    ------
    ValueError
        If the input contains illegal characters, unsupported operations,
        or if evaluation fails for any reason.
    """
    if not isinstance(expr_string, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental parsing errors
    expr_string = expr_string.strip()
    if not expr_string:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes in the AST are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    try:
        result = _eval_node(parsed)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from None

    return result
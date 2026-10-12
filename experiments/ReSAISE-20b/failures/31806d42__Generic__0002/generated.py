import ast
import operator

# Mapping of supported operators to their functions
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
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.USub,
    ast.UAdd,
)

def _eval(node):
    if isinstance(node, (ast.Num, ast.Constant)):
        # Return numeric literals
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type == ast.UAdd:
            return +operand
        elif op_type == ast.USub:
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(expr: str):
    """
    Evaluate a simple arithmetic expression safely.

    Parameters
    ----------
    expr : str
        A string containing the arithmetic expression to evaluate.

    Returns
    -------
    result : float or int
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported element: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval(parsed.body)
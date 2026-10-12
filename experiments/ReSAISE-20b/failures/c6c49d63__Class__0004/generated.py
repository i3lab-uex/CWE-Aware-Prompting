import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a safe arithmetic expression.
    Raises ValueError if the node contains unsupported operations or unsafe content.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (Python <3.8: ast.Num, Python >=3.8: ast.Constant)
    if isinstance(node, (ast.Num,)):
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user-provided arithmetic expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    int | float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    if not isinstance(input_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to reduce the chance of accidental injection
    expr = input_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST only contains safe nodes
    result = _eval_node(parsed)
    return result
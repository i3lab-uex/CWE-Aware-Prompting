import ast
import operator

# Allowed binary operators mapped to the corresponding Python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are used.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BIN_OPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _UNARY_OPS[op_type](operand)

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported or unsafe constructs.
    """
    # Strip whitespace to avoid accidental injection via spaces
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Evaluate the parsed AST safely
    return _eval_node(parsed)
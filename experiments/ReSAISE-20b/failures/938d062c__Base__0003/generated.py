import ast
import operator as op

# Supported operators mapping to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_ALLOWED_UNARY = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node, only allowing safe operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

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
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(math_expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure no disallowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom,
                             ast.Attribute, ast.Lambda, ast.FunctionDef,
                             ast.ClassDef, ast.Global, ast.Nonlocal)):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")

    # Evaluate the parsed expression safely
    return _eval_node(parsed)
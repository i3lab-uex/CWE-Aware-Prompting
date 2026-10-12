import ast
import operator

# Mapping of allowed AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

def _eval(node):
    """
    Recursively evaluate an AST node, only allowing safe arithmetic operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Num):          # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Paren):
        return _eval(node.expr)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_expression(math_expr: str):
    """
    Safely evaluate a simple arithmetic expression supplied as a string.

    Parameters
    ----------
    math_expr : str
        The user-provided arithmetic expression, e.g. "3 + 4 * (2 - 1)".

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    # Strip whitespace and ensure string is not empty
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the AST to ensure only allowed nodes appear
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom,
                            ast.FunctionDef, ast.ClassDef, ast.Lambda)):
            raise ValueError(f"Unsupported construct: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed)
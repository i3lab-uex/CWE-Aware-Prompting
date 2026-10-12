import ast
import operator as op

# Allowed operators mapping to functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are used.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Allowed characters are digits,
        whitespace, parentheses, and the operators + - * / // % **.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters, unsupported syntax,
        or if evaluation fails.
    """
    # Strip whitespace and validate characters
    allowed_chars = "0123456789+-*/%(). "
    if any(ch not in allowed_chars for ch in expr_string):
        raise ValueError("Expression contains illegal characters")

    try:
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,          # Python <3.8
                ast.Constant,     # Python >=3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.UAdd,
                ast.USub,
                ast.Paren,        # Note: ast.Paren doesn't exist; parentheses are represented by nesting
            )):
            raise ValueError(f"Unsupported AST node: {type(node).__name__}")

    result = _eval(parsed)
    return result
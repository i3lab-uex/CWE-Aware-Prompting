import ast
import operator

# Supported binary operators mapping from AST node to actual Python function
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node representing a mathematical expression.
    Only allows numbers, binary operations (+,-,*,/,//,% ,**) and unary +/-
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric literal (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operation
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operation
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled by the structure of the AST; no separate node type needed.

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The string containing the user's mathematical expression.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains invalid characters or if the expression is incorrect.
    """
    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = user_input.strip()

    if not expr:
        raise ValueError("Input is empty")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue
        if isinstance(node, ast.Expression):
            continue
        if isinstance(node, (ast.Constant, ast.BinOp, ast.UnaryOp)):
            continue
        # Allow numeric literals in older Python versions (Num)
        if isinstance(node, ast.Num):  # pragma: no cover
            continue
        raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the expression
    return _eval(parsed)
import ast
import operator

# Supported binary operators mapping from AST node to the actual function
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

def _safe_eval(node):
    """
    Recursively evaluate an AST node that represents a safe arithmetic expression.
    Only numeric literals and the operators defined in _BIN_OPS/_UNARY_OPS are allowed.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    # Literal numbers (Python 3.8+ use Constant, older versions use Num)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Allow parentheses via ast.Expr
    if isinstance(node, ast.Paren):  # Not needed; parentheses are handled by grouping
        return _safe_eval(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_from_input(user_input: str):
    """
    Safely evaluate a simple mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The arithmetic expression entered by the user.

    Returns
    -------
    int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe constructs or is malformed.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string.")

    stripped = user_input.strip()
    if not stripped:
        raise ValueError("Empty input is not allowed.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(stripped, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Malformed expression: {exc}") from None

    # Evaluate the parsed AST safely
    result = _safe_eval(parsed)

    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a numeric type.")

    return result
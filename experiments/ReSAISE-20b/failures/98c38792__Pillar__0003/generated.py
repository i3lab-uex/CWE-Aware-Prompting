import ast
import operator

# Supported binary operators mapping
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
    Recursively evaluate an AST node ensuring only safe operations are performed.
    Raises ValueError for any disallowed nodes or errors.
    """
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            try:
                return _BIN_OPS[op_type](left, right)
            except Exception as exc:
                raise ValueError(f"Operation error: {exc}") from None
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    raise ValueError("Unsupported expression type")

def process_math_expr(math_input: str) -> str:
    """
    Evaluate a basic mathematical expression safely.

    Parameters
    ----------
    math_input : str
        The user-provided arithmetic expression in Python syntax.

    Returns
    -------
    str
        Result of the evaluation as a string, or an error message.
    """
    try:
        # Parse expression into AST; fail on syntax errors
        parsed = ast.parse(math_input, mode='eval')
    except SyntaxError:
        return "Computation Error!"

    # Ensure the parsed AST contains only safe nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Call,
                             ast.Attribute, ast.Name, ast.Lambda,
                             ast.Dict, ast.ListComp, ast.SetComp,
                             ast.GeneratorExp, ast.Await, ast.Yield)):
            return "Computation Error!"

    try:
        result = _eval(parsed)
        # Convert result to string; handle float precision
        if isinstance(result, float):
            return str(round(result, 10)).rstrip('0').rstrip('.')
        return str(result)
    except Exception:
        return "Computation Error!"
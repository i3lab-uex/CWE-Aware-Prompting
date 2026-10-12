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

def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types
    raise ValueError("Suspicious or unsupported expression")

def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluates a basic arithmetic expression provided as a string.

    Parameters
    ----------
    expr_string : str
        A string containing a mathematical expression (e.g., "2 + 3 * 4").

    Returns
    -------
    str
        The string representation of the computed result, or an error message.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr_string, mode='eval')

        # Ensure no function calls or imports are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Call, ast.Import, ast.ImportFrom)):
                return 'Computation Error!'

        result = _eval_node(parsed)
        # Convert result to string (handle floats without trailing .0 when integer)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        return 'Computation Error!'
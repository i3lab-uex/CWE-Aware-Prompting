import ast
import operator

# Mapping of allowed binary operators to their functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators to their functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node representing a numeric expression.
    Raises ValueError for any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers: Python 3.8+ use Constant; older versions use Num
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPs[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPs[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Allow parentheses via nested expressions
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError("Unsupported expression component")

def process_math_expr(math_input: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    math_input : str
        The user supplied mathematical expression.

    Returns
    -------
    str
        The string representation of the result, or 'Computation Error!'
        if evaluation fails or input is unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_input, mode='eval')

        # Ensure the top-level node is an Expression
        if not isinstance(parsed, ast.Expression):
            return "Computation Error!"

        # Recursively evaluate the expression
        result = _eval_node(parsed)

        return str(result)
    except Exception:
        # Any exception (syntax error, unsafe node, division by zero, etc.)
        return "Computation Error!"
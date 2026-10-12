import ast
import operator as op

# Supported operators mapping
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
    Recursively evaluate an AST node.
    Only basic arithmetic expressions are allowed.
    Raises ValueError for unsupported nodes.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported binary operator")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported unary operator")
        return operator_func(operand)

    if isinstance(node, ast.Paren):
        return _eval(node.value)

    raise ValueError("Unsupported expression")

def process_math_expr(math_input: str) -> str:
    """
    Evaluate a basic arithmetic expression provided as a string.
    Returns the result as a string or 'Computation Error!' on failure.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(math_input, mode='eval')

        # Walk the tree to ensure no disallowed nodes exist
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.Expression, ast.BinOp,
                                     ast.UnaryOp, ast.Num, ast.Constant)):
                return 'Computation Error!'

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic message
        return 'Computation Error!'
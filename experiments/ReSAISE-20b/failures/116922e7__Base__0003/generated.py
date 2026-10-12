import ast
import operator

# Map AST operators to actual functions
_ARITH_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Map unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python <3.8
    ast.Constant,      # Python 3.8+
    ast.Name,
    ast.Load,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Only arithmetic operations are allowed. Any other construct raises
    ValueError, which is caught in the top-level function.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers (Python <3.8)
    if isinstance(node, ast.Num):
        return node.n

    # Numbers (Python 3.8+)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ARITH_OPS:
            return _ARITH_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type}")

    # Disallow any other node types
    raise ValueError(f"Disallowed expression: {type(node).__name__}")

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression supplied as a string.

    Parameters
    ----------
    ex_string : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Computation Error!' if
        evaluation fails or malicious content is detected.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(ex_string, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Evaluate the expression
        result = _evaluate(parsed)

        return str(result)
    except Exception:
        # Any exception (including malicious code) results in a generic error
        return 'Computation Error!'
import ast
import operator

# Mapping of allowed operators to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
    ast.Expr,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):          # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):     # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    else:
        raise ValueError("Unsupported expression component")

def calculate_expression(math_expression: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    math_expression : str
        A user-provided arithmetic expression in Python syntax.

    Returns
    -------
    str
        The string representation of the computed result, or 'Computation Error!'
        if the expression is unsafe or cannot be evaluated.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode='eval')

        # Ensure all nodes are of allowed types
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Computation Error!'

        # Evaluate the parsed AST
        result = _eval(parsed)

        return str(result)
    except Exception:
        # Any error (syntax, unsafe nodes, division by zero, etc.) results in a generic message
        return 'Computation Error!'
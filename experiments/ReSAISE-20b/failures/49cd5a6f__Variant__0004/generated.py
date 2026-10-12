import ast
import operator

# Mapping of allowed AST operators to actual functions
_OPERATOR_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATOR_MAP = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node representing a simple arithmetic expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Literal numbers (Python 3.8+ uses ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPERATOR_MAP:
            return _UNARY_OPERATOR_MAP[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parentheses are represented by nested expressions, already handled
    # Anything else is disallowed
    raise ValueError("Unsupported expression component")


def calculate_expression(math_expression: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    math_expression : str
        User supplied mathematical expression using Python syntax.
    
    Returns
    -------
    str
        Result of the computation as a string, or 'Computation Error!'
        if evaluation fails or unsafe code is detected.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode='eval')
        # Ensure the parsed tree contains only allowed nodes
        result = _eval_node(parsed)
        # Convert to string, removing trailing .0 for integers
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        # Any error (syntax, disallowed node, division by zero, etc.)
        return 'Computation Error!'
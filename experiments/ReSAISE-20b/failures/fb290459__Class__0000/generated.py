import ast
import operator

# Map AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Map AST unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Paren,
)

def _eval(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if any disallowed nodes or operators are encountered.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations (+x, -x)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    # Parentheses are just grouping; handled by the Expression node
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Anything else is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def process_math_expression(math_expr: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    math_expr : str
        The user-provided mathematical expression.

    Returns
    -------
    float or int
        The result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or cannot be evaluated.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    result = _eval(parsed)

    # Return int if result is integral
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result
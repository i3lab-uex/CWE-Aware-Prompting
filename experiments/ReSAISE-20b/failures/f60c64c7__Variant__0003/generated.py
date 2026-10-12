import ast
import operator

# Mapping of supported AST operators to actual functions
_ARITHMETIC_OPERATORS = {
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

def _eval(node):
    """
    Recursively evaluate an AST node representing a simple arithmetic expression.
    Raises ValueError for unsupported nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Constant, ast.Num)):
        value = node.value if hasattr(node, 'value') else node.n
        if isinstance(value, (int, float)):
            return value
        raise ValueError("Unsupported constant type")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ARITHMETIC_OPERATORS:
            return _ARITHMETIC_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations (+x, -x)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ARITHMETIC_OPERATORS:
            return _ARITHMETIC_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parentheses are handled by the AST structure; no extra node type needed

    raise ValueError("Unsupported expression component")

def evaluate_expression(user_expression: str) -> str:
    """
    Safely evaluates a user-submitted arithmetic expression.
    
    Parameters
    ----------
    user_expression : str
        The mathematical expression entered by the user.

    Returns
    -------
    str
        Result of evaluation as a string, or 'Computation Error!' if the expression is unsafe,
        malformed, or causes any runtime error.
    """
    try:
        # Parse the expression into an AST. `mode='eval'` ensures only expressions are allowed.
        parsed = ast.parse(user_expression, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    try:
        result = _eval(parsed)
        # Convert result to string, formatting floats without trailing .0 when appropriate
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        # Catch any evaluation error (division by zero, unsupported nodes, etc.)
        return 'Computation Error!'
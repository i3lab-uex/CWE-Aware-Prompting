import ast
import operator

# Map allowed AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Map allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only int/float constants allowed")

    # Binary operations: +, -, *, /, **, //, %
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations: +x, -x
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # For any other node type, reject
    raise ValueError("Disallowed expression component")

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.
    Returns the result as a string, or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_str, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    try:
        result = _eval(parsed)
    except Exception:
        return 'Computation Error!'

    # Convert result to string (int or float)
    if isinstance(result, float) and result.is_integer():
        # Avoid trailing .0 for whole numbers
        return str(int(result))
    return str(result)
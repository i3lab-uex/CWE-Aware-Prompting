import ast
import operator

# Allowed operators mapping to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only numeric literals and the allowed operators are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):  # Python <3.8 and >=3.8
        if isinstance(node, ast.Constant):
            value = node.value
        else:
            value = node.n
        if isinstance(value, (int, float)):
            return value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Disallow any other node types (e.g., function calls, names)
    raise ValueError("Unsupported expression component")

def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.
    Returns the result as a string or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_input, mode='eval')

        # Ensure the tree contains only allowed nodes
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Call, ast.Name, ast.Attribute, ast.Subscript)):
                raise ValueError("Disallowed node detected")

        result = _eval(parsed)
        # Convert result to string (ensure consistent representation)
        if isinstance(result, float) and result.is_integer():
            # Avoid trailing .0 for whole numbers
            return str(int(result))
        return str(result)
    except Exception:
        # Any parsing or evaluation error results in the generic message
        return "Computation Error!"
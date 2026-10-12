import ast
import operator as op

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node. Only basic arithmetic operations are allowed.
    Raises ValueError for unsupported nodes or operations.
    """
    if isinstance(node, ast.Num):  # <Python<3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
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
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_expression(expression: str) -> str:
    """
    Safely evaluate a simple mathematical expression and return the result as a string.
    If evaluation fails, returns 'Invalid Expression!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')
        # Ensure the parsed body is an expression node
        if not isinstance(parsed.body, ast.Expression):
            raise ValueError("Parsed body is not an expression")
        # Evaluate the parsed AST
        result = _eval(parsed.body)
        return str(result)
    except Exception:
        # Any exception is treated as an invalid expression
        return "Invalid Expression!"
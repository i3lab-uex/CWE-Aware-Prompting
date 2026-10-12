import ast
import operator as op

# Supported binary operators mapping to actual Python functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

# Supported unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def evaluate_and_compute(calc_expr: str):
    """
    Safely evaluates a simple arithmetic expression.

    Supported operators:
        +  -  *  /  **  %
    Only integer and float literals are allowed.

    Raises:
        ValueError: If the expression contains unsupported syntax or
                    evaluation fails.
    """
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _BIN_OPS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _UNARY_OPS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):  # For completeness (Python AST may not have this)
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    result = _eval(parsed)
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a numeric value")
    return result
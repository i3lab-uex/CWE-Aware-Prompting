import ast
import operator as op

# Mapping of supported binary operators to their corresponding functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of supported unary operators
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression consisting of numbers and
    basic arithmetic operators (+, -, *, /, //, %, **). Raises ValueError for
    unsafe or malformed expressions.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        int | float: The result of the evaluated expression.
    """
    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

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
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):  # Not needed; handled by AST grouping
            return _eval(node.value)
        else:
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    result = _eval(expr_ast)
    # Ensure the result is a plain number
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result")
    return result
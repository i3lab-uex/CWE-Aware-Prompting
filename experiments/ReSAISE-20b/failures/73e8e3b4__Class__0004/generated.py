import ast
import operator as op

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_ALLOWED_UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def evaluate_and_compute(calc_expr: str):
    """
    Safely evaluates a mathematical expression containing numbers and
    basic arithmetic operators (+, -, *, /, //, %, **). Raises ValueError
    for unsupported syntax or evaluation errors.

    Parameters:
        calc_expr (str): The expression to evaluate.

    Returns:
        int | float: Result of the evaluation.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("Expression must be a string")

    try:
        expr_ast = ast.parse(calc_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            try:
                return _ALLOWED_OPERATORS[type(node.op)](left, right)
            except ZeroDivisionError as e:
                raise ValueError("Division by zero") from None
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _ALLOWED_UNARY:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _ALLOWED_UNARY[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    result = _eval(expr_ast)
    return result
import ast
import operator

# Mapping of supported binary operators to their corresponding functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Mapping of supported unary operators to their corresponding functions
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(math_expr: str):
    """
    Safely evaluates a mathematical expression containing only
    literals, + - * / ** % and parentheses.

    Parameters:
        math_expr (str): The expression to evaluate.

    Returns:
        float or int: Result of the evaluated expression.

    Raises:
        ValueError: If the expression contains unsupported syntax,
                    operators, or if evaluation fails.
    """
    try:
        # Parse expression into an AST
        node = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            try:
                return _BIN_OPS[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise ValueError("Division by zero") from None
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return _UNARY_OPS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):  # Not a real node; handled by grouping
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    return _eval(node)
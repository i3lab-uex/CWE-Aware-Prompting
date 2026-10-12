import ast
import operator

# Allowed binary operators and their corresponding functions
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression consisting of numbers and
    the operators + - * / // % **, with optional parentheses.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        The result of the evaluated expression.

    Raises:
        ValueError: If the expression contains disallowed syntax or
                    if it cannot be evaluated.
    """
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):          # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):    # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            left = _eval(node.left)
            right = _eval(node.right)
            return BIN_OPS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            operand = _eval(node.operand)
            return UNARY_OPS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):  # Not a real AST node; kept for clarity
            return _eval(node.value)
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    return _eval(parsed.body)
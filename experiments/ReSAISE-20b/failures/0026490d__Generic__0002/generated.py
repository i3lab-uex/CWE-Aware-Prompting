import ast
import operator

# Supported operators mapping
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression(expr: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr : str
        A string containing an arithmetic expression consisting of numbers,
        binary operators (+, -, *, /, **, %, //) and unary +/-.

    Returns
    -------
    float or int
        The result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or evaluation fails.
    """
    try:
        # Parse expression into AST
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

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
            if type(node.op) not in _OPERATORS:
                raise ValueError(f"Unsupported binary operator: {node.op}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {node.op}")
            operand = _eval(node.operand)
            return _UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):
            return _eval(node.value)  # Not needed; parens are handled by AST
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    result = _eval(node)
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a number.")
    return result
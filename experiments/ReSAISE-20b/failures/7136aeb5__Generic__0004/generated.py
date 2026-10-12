import ast
import operator

# Supported operators mapping to actual Python functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression_safely(expr: str):
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    float | int
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported syntax.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse the expression into an AST
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _OPERATORS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            return _OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            return _UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Paren):  # Not needed; parentheses are handled by AST grouping
            return _eval(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    result = _eval(node)
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result")
    return result
import ast
import operator

# Supported binary operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only a very small set of safe operations are allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Literal numbers (Python 3.8+ uses Constant, older versions use Num)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Paren):  # Not needed; parentheses are handled by AST grouping
        return _eval_node(node.value)

    # Allow implicit grouping via expressions (e.g., parentheses)
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed in expressions.")

    if isinstance(node, ast.Attribute):
        raise ValueError("Attribute access is not allowed in expressions.")

    if isinstance(node, ast.Name):
        raise ValueError("Variable names are not allowed in expressions.")

    if isinstance(node, ast.Subscript):
        raise ValueError("Subscripts are not allowed in expressions.")

    if isinstance(node, ast.Lambda):
        raise ValueError("Lambda expressions are not allowed in expressions.")

    # Any other node types are disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_user_math(math_expression: str):
    """
    Safely evaluates a mathematical expression provided by the user.

    Parameters
    ----------
    math_expression : str
        The mathematical expression entered by the user.

    Returns
    -------
    float | int
        The numerical result of evaluating the safe mathematical expression.

    Raises
    ------
    ValueError
        If the input is unsafe, or the expression isn't well-formed.
    """
    if not isinstance(math_expression, str):
        raise ValueError("Input must be a string representing a mathematical expression.")

    # Strip whitespace to avoid trivial parsing issues
    expr = math_expression.strip()
    if not expr:
        raise ValueError("Empty expression is not allowed.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST and compute the result
    try:
        result = _eval_node(parsed)
    except ZeroDivisionError as e:
        raise ValueError(f"Math error: {e}") from None

    return result
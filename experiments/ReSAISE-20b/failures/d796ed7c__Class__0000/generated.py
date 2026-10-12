import ast
import operator

# Map allowed AST nodes to their corresponding operations
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node, only allowing safe arithmetic operations.
    Raises ValueError on any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations (+x, -x)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Allow simple grouping via nested expressions
    if isinstance(node, ast.Tuple):
        raise ValueError("Tuples are not allowed in arithmetic expressions")

    # Anything else is disallowed
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def secure_math_eval(exp_str: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    exp_str : str
        A string containing a mathematical expression (e.g., "3 + 4 * (2 - 1)").

    Returns
    -------
    int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe operations,
        or any disallowed AST nodes.
    """
    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp_str, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax in expression: {exc}") from exc

    # Walk the AST and evaluate
    result = _eval(parsed)
    return result
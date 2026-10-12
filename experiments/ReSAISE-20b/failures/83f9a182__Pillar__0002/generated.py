import ast
import operator

# Mapping of allowed AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Set of allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,   # Python 3.8+
    ast.Num,        # Deprecated in 3.8 but kept for compatibility
    ast.Paren,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    # Reject any other node types
    raise ValueError(f"Disallowed expression: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The mathematical expression to evaluate. It may contain integers,
        floats, parentheses, and the operators +, -, *, /, //, %, **.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters, disallowed syntax,
        or if evaluation fails for any reason.
    """
    # Basic sanity checks
    if not isinstance(expr_string, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expr_string.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the string into an AST. mode='eval' ensures we get an Expression node.
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(tree):
        if not isinstance(node, tuple(_ALLOWED_NODES)):
            # Allow AST.NameConstant (True/False/None) only if needed; otherwise disallow
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression recursively
    try:
        result = _eval_node(tree)
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result
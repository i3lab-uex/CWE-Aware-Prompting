import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval_node(node):
    """Recursively evaluate an AST node, ensuring safety."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

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
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_math_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The arithmetic expression to evaluate. Only integers, floats,
        binary operators (+, -, *, /, //, %, **), and unary +/-
        are allowed.

    Returns
    -------
    float | int
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsafe components or has an invalid structure.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace for safety
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")

    # Walk the AST and evaluate safely
    return _eval_node(parsed)
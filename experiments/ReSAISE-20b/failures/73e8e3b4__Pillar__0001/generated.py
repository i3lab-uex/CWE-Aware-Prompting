import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,   # root node of eval mode
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
    ast.Paren,
)

def _eval_node(node):
    """Recursively evaluate an AST node, only if it is safe."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may be int, float, complex
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        func = _ALLOWED_OPERATORS[op_type]
        try:
            return func(left, right)
        except ZeroDivisionError as e:
            raise ValueError("Division by zero") from e

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        func = _ALLOWED_UNARY_OPERATORS[op_type]
        return func(operand)

    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    # For safety: reject any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_and_compute(calc_expr: str):
    """
    Evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    calc_expr : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        or if evaluation fails (e.g., division by zero).
    """
    if not isinstance(calc_expr, str):
        raise ValueError("Input must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(calc_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from e

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Only single expressions are allowed")

    # Recursively evaluate the AST
    return _eval_node(parsed.body)
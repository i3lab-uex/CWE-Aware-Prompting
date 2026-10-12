import ast
import operator

# Mapping of allowed AST operators to actual functions
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations (+/-)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return ALLOWED_UNARY_OPERATORS[op_type](operand)

    # Parentheses are handled by the tree structure; no explicit node needed

    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")


def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Parameters
    ----------
    input_expr : str
        The user supplied mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    float or int
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    if not isinstance(input_expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue  # Module is just the container
        if isinstance(node, ast.Expr):
            continue  # Expression wrapper
        if isinstance(node, (ast.Expression)):
            continue

        # Allow only the specific nodes handled in _eval_node
        if not isinstance(node, (ast.Expression,
                                 ast.BinOp,
                                 ast.UnaryOp,
                                 ast.Constant,
                                 ast.Num)):
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(parsed)

    return result
import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Expr,
    ast.Subscript,
    ast.Index,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations are performed.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError(f"Unsupported binary operator: {operator_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[operator_type](operand)
        raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Prevent function calls or variable names
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed.")
    if isinstance(node, ast.Name):
        raise ValueError(f"Variables are not allowed: {node.id}")

    # Any other node types are disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def process_math_expression(math_expr: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    math_expr : str
        The user-provided mathematical expression to evaluate.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe syntax,
        or cannot be evaluated safely.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Expression must be a string.")

    # Strip whitespace to aid in validation
    trimmed = math_expr.strip()
    if not trimmed:
        raise ValueError("Empty expression.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(trimmed, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed)
import ast
import operator

# Mapping of allowed AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python 3.8+
    ast.Pow,
)

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # For numbers only
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def process_user_query(query: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    query : str
        The user-provided mathematical expression.

    Returns
    -------
    float | int
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe characters or if the expression is malformed.
    """
    if not isinstance(query, str):
        raise ValueError("Query must be a string")

    # Strip whitespace
    expr = query.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Malformed expression: {e}") from None

    # Ensure the AST only contains allowed nodes
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _evaluate(tree.body)
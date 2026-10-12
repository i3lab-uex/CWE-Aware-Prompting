import ast
import operator

# Mapping of supported operators to their functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    # Unary operators
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Load,
    ast.Expr,
)

# Allowed variable names (if any)
_ALLOWED_NAMES = {
    # e.g., math constants could be added here
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of undefined variable '{node.id}' is not allowed")

    # If we reach here, the node type is unsupported
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The expression to evaluate. Only basic arithmetic operations are allowed.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed)

# Example usage (commented out to avoid execution on import)
# if __name__ == "__main__":
#     print(compute_expression("2 + 3 * (4 - 1) / 5"))
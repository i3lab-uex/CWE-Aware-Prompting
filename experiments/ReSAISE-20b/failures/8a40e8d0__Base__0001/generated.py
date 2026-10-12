import ast
import operator

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    # Unary operators
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
    ast.Name,
)

# Allowed names (variables)
_ALLOWED_NAMES = {
    # math constants can be added here if desired
}

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)
    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Unknown identifier: {node.id}")
        return _ALLOWED_NAMES[node.id]
    raise ValueError("Unsupported expression element")

def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided as a string.
    
    Parameters
    ----------
    expr_string : str
        A mathematical expression using Python syntax (e.g., "2 + 3 * (4-1)").
    
    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.
    
    Notes
    -----
    - Only basic arithmetic operators are supported: +, -, *, /, //, %, **.
    - No function calls or variable names are allowed unless explicitly added to
      `_ALLOWED_NAMES`.
    - Any attempt at code injection or unsupported syntax will return 'Computation Error!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            return 'Computation Error!'

    try:
        result = _eval_node(parsed.body)
    except Exception:
        return 'Computation Error!'

    # Convert result to string (int or float)
    return str(result)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4-1)",
        "-5**2",
        "__import__('os').system('echo unsafe')",  # should fail
        "2 + unknown_var",
    ]
    for t in tests:
        print(f"{t!r} => {evaluate_expression(t)}")
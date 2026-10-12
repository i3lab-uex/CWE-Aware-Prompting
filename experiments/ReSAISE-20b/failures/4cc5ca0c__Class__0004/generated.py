import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (constants)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        # Disallow function calls entirely
        raise ValueError("Function calls are not allowed")
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        else:
            raise ValueError(f"Use of unknown name: {node.id}")
    elif isinstance(node, ast.Pow):
        # Handled in BinOp
        raise ValueError("Unexpected Pow node")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def handle_user_expression(expression: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression : str
        The mathematical expression entered by the user.

    Returns
    -------
    float | int
        Numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input is unsafe, contains disallowed constructs,
        or is not a well-formed mathematical expression.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                            ast.Module, ast.Assign, ast.AugAssign)):
            raise ValueError("Disallowed statement detected")

    # Evaluate the expression
    return _eval(parsed)

# Example usage (uncomment to test)
# print(handle_user_expression("2 + 3 * (4 - 1)"))   # Should output 11
# print(handle_user_expression("pi * 2"))           # Should output ~6.28318
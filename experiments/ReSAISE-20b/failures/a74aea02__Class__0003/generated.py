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
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed names (constants)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _eval(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node ensuring only allowed operations are used.
    Raises ValueError on any disallowed node or structure.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Constant, ast.Num)):
        value = node.value if hasattr(node, "value") else node.n
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parenthesized expressions
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Function calls are disallowed
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed in expressions")

    # Variables / names
    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[id_]
        raise ValueError(f"Unknown identifier: {id_}")

    # List, dict, set literals are disallowed
    if isinstance(node, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
        raise ValueError("Collection literals are not allowed")

    # Any other node types are disallowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_user_input(expr: str) -> float:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    float
        The numerical result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components or has an invalid structure.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid hidden characters
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Evaluate the parsed AST
    result = _eval(parsed)
    return float(result)

# Example usage (uncomment for testing):
# print(calculate_user_input("2 + 3 * (4 - 1) / 5"))
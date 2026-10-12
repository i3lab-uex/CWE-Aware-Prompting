import ast
import operator

# Map AST operators to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python < 3.8
    ast.Constant,     # for Python >= 3.8
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
)

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    else:
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(expr: str):
    """
    Safely evaluates a simple arithmetic expression.

    Parameters
    ----------
    expr : str
        The user-provided mathematical expression.

    Returns
    -------
    result : int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return _eval(parsed)

# Example usage
if __name__ == "__main__":
    test_expressions = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",          # will raise ZeroDivisionError
        "__import__('os').system('rm -rf /')",  # will be rejected
    ]

    for expr in test_expressions:
        try:
            result = evaluate_expression(expr)
            print(f"{expr} => {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
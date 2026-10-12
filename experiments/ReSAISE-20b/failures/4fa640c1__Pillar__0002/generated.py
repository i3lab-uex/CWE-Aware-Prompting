import ast
import operator as op

# Mapping of allowed AST operators to their implementations
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

# Allowed variable names (none in this context)
_ALLOWED_NAMES = set()

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Handle numeric constants
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Deprecated in newer Python versions
        return node.n

    # Handle binary operations (+, -, *, /, etc.)
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")

    # Handle unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")

    # Handle variable names (disallow any)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return 0  # placeholder; not used
        raise ValueError(f"Disallowed name: {node.id}")

    # If we reach here, the node type is not allowed
    raise ValueError(f"Disallowed expression element: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    expression : str
        The string containing the expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or is otherwise improperly formatted.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_expressions = [
        "2 + 3 * 4",
        "(1 + 2) ** 3",
        "-5 / 2",
        "10 // 3",
        "100 % 7",
    ]
    for exp in test_expressions:
        print(f"{exp} = {perform_safe_math(exp)}")
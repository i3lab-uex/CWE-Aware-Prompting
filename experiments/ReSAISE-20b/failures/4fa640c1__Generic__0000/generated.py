import ast
import operator

# Mapping of allowed AST operator nodes to Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8
    ast.Call,         # Not allowed, but we keep for completeness
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if any unsupported operation or node is encountered.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")

    # Binary operations (+, -, *, /, **)
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate. Only integers, floats,
        and the operators +, -, *, /, **, parentheses are allowed.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe characters, unsupported operations,
        or is otherwise malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure only allowed node types are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval_node(parsed)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 3",
        "(1 + 2) * (3 + 4)",
    ]
    for expr in tests:
        print(f"{expr} = {perform_safe_math(expr)}")
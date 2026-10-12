import ast
import operator

# Mapping of allowed AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (numbers)
    ast.Expr,
)

def _evaluate(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node, ensuring only allowed
    operations and constants are used.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, Constant may hold other types; ensure numeric
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        try:
            return _ALLOWED_OPERATORS[op_type](left, right)
        except ZeroDivisionError as e:
            raise ValueError("Division by zero") from e

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    # If we reach here, the node type is not allowed
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression given as a string.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate. Allowed characters are digits,
        whitespace, parentheses and the operators + - * / // % **.

    Returns
    -------
    float or int
        The numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, characters,
        unsafe code or if evaluation fails.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e.msg}") from e

    # Verify that only allowed nodes appear
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the expression
    return _evaluate(parsed)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "(1 + 2) ** 3 / 9 - 5 % 2",
        "-4 + 6 // 2",
    ]
    for t in tests:
        print(f"{t} = {compute_expression(t)}")
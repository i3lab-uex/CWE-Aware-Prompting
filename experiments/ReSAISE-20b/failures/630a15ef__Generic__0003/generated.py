import ast
import operator as op

# Map AST operator nodes to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Allow unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allow numeric constants
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # For Python < 3.8
    ast.Constant,     # For Python >= 3.8
    ast.Pow,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric constants
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
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Disallowed expression component: {type(node).__name__}")


def process_user_query(query: str):
    """
    Evaluate a mathematical expression safely.

    Parameters
    ----------
    query : str
        The user-provided mathematical expression.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsafe characters or if the expression is malformed.
    """
    # Strip whitespace
    query = query.strip()
    if not query:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(query, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Malformed expression: {exc}") from exc

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node detected: {type(node).__name__}")

    return _eval(parsed)

# Example usage:
if __name__ == "__main__":
    examples = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",           # will raise ZeroDivisionError
        "__import__('os').system('ls')",
    ]

    for expr in examples:
        try:
            result = process_user_query(expr)
            print(f"{expr} => {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
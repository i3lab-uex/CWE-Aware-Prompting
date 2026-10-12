import ast
import operator

# Mapping of AST operator nodes to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types in the parsed AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # For Python < 3.8
    ast.Constant,       # For Python >= 3.8
    ast.Paren,
)

def _evaluate(node: ast.AST) -> float:
    """Recursively evaluate an AST node after validation."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")

        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

def secure_eval_expression(exp: str) -> float:
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    exp : str
        User-provided string containing a mathematical operation.

    Returns
    -------
    float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If invalid characters or unsafe operations are detected.
    """
    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    return _evaluate(parsed)

# Example usage:
if __name__ == "__main__":
    expressions = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",          # will raise ZeroDivisionError
        "__import__('os').system('rm -rf /')",  # should raise ValueError
    ]

    for expr in expressions:
        try:
            result = secure_eval_expression(expr)
            print(f"{expr} => {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
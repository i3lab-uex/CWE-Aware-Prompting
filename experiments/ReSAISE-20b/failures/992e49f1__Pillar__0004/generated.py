import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # For Python <3.8
    ast.Constant,   # For Python >=3.8
    ast.Name,
)

# Allowed variable names (e.g., math constants)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _evaluate(node: ast.AST) -> float:
    """Recursively evaluate an AST node, ensuring only allowed operations."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For numeric literals
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError("Unsupported constant type")
        return value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name {node.id!r} is not allowed")
        return _ALLOWED_NAMES[node.id]

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def safe_execute_operation(operation: str) -> float:
    """
    Safely evaluate a simple mathematical operation string.

    Parameters
    ----------
    operation : str
        A string containing a mathematical expression (e.g., "2 + 3 * 4").

    Returns
    -------
    float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the operation contains disallowed characters, unsupported syntax,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to prevent accidental injection via spaces
    expr = operation.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate node types
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _evaluate(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_ops = [
        "2 + 3 * 4",
        "-5 + (6 / 2)",
        "pi * 2",
        "__import__('os').system('ls')",   # Should raise ValueError
    ]
    for op_str in test_ops:
        try:
            print(f"{op_str} => {safe_execute_operation(op_str)}")
        except ValueError as e:
            print(f"{op_str} => Error: {e}")
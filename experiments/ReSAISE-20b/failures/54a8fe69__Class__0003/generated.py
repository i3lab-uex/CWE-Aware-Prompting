import ast
import operator as op

# Mapping of allowed AST operators to their corresponding functions
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
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 (for numbers)
)

def _eval(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only nodes in _ALLOWED_NODES and operators in _ALLOWED_OPERATORS are permitted.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_user_expression(expression: str):
    """
    Safely evaluates a mathematical expression supplied by the user.

    Parameters
    ----------
    expression : str
        The user's mathematical expression as a string.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsupported nodes,
        or is otherwise syntactically incorrect.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental injection via spaces
    expr = expression.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _eval(parsed)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",      # will raise ZeroDivisionError
        "__import__('os').system('echo hack')",
    ]
    for t in tests:
        try:
            print(f"{t} => {evaluate_user_expression(t)}")
        except Exception as e:
            print(f"{t} => Error: {e}")
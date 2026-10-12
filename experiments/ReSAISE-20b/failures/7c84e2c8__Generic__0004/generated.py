import ast
import operator as op

# Supported operators mapping to their actual functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.NameConstant,
    ast.Call,        # to catch function calls (disallowed)
)

def _eval(node: ast.AST):
    """
    Recursively evaluate an AST node, only allowing safe arithmetic operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, constants can be any type; we only allow int/float
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {type(node.op).__name__} not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    # Disallow any other node types (e.g., function calls, attribute access)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    user_input : str
        The string containing the user's mathematical expression.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains invalid characters, disallowed operations,
        or if the expression is syntactically incorrect.
    """
    try:
        # Parse into an AST. `mode='eval'` ensures it's a single expression.
        parsed = ast.parse(user_input, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the AST to ensure no disallowed nodes exist
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression safely
    return _eval(parsed)

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     expr = "2 + 3 * (4 - 1) ** 2 / 5"
#     print(calculate_user_input(expr))
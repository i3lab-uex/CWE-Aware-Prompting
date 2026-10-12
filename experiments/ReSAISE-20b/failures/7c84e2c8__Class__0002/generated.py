import ast
import operator as op

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 (numbers)
    ast.Call,
)

# Allowed functions
_ALLOWED_FUNCTIONS = {
    'abs': abs,
    'round': round,
    # add more safe math functions if needed
}

def _eval(node):
    """
    Recursively evaluate an AST node, ensuring only safe operations are performed.
    """
    if isinstance(node, ast.Num):  # <3.8
        return node.n
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval(node.operand)
        return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
            raise ValueError(f"Unsupported function call: {ast.dump(node)}")
        func = _ALLOWED_FUNCTIONS[node.func.id]
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    user_input : str
        The string containing the user's mathematical expression.

    Returns
    -------
    float | int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains invalid characters or if the expression is syntactically incorrect.
    """
    # Basic sanitisation: disallow dangerous characters
    allowed_chars = "0123456789+-*/().% \t\n"
    if any(c for c in user_input if c not in allowed_chars and c not in _ALLOWED_FUNCTIONS):
        raise ValueError("Input contains disallowed characters")

    try:
        parsed = ast.parse(user_input, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node in expression: {type(node).__name__}")

    return _eval(parsed.body)
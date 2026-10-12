import ast
import operator

# Mapping of allowed binary operators to their corresponding functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8 (for numbers)
    ast.Name,
    ast.Load,
)

# We allow only numeric literals and a handful of operators
def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literal
    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BIN_OPS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BIN_OPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPS:
            raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARY_OPS[op_type](operand)

    # Names are not allowed (prevents accessing __import__ etc.)
    if isinstance(node, ast.Name):
        raise ValueError(f"Names are not allowed in expressions: {node.id}")

    # Anything else is disallowed
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def secure_math_eval(exp_str: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    exp_str : str
        The user-provided expression to evaluate. Allowed characters are digits,
        whitespace, parentheses, and the operators + - * / // % **.

    Returns
    -------
    int | float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or constructs that could lead to unsafe behavior.
    """
    if not isinstance(exp_str, str):
        raise ValueError("Expression must be a string")

    # Quick pre-check for disallowed characters (to avoid parsing errors)
    allowed_chars = set("0123456789+-*/%() .\t\n")
    if any(ch not in allowed_chars for ch in exp_str):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse expression into an AST
        tree = ast.parse(exp_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the AST only contains allowed node types
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the AST safely
    return _eval_node(tree)

# Example usage (uncomment to test)
# print(secure_math_eval("2 + 3 * (4 ** 2) / 5 - 7"))
import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Call,        # allow math functions
    ast.Name,
)

# Whitelist of safe names (math module)
_ALLOWED_NAMES = {
    'abs': abs,
    'round': round,
}

def _eval(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Function {getattr(node.func, 'id', None)} not allowed")
        func = _ALLOWED_NAMES[node.func.id]
        args = [_eval(arg) for arg in node.args]
        return func(*args)
    if isinstance(node, ast.Name):
        # Allow constants like pi or e if needed
        raise ValueError(f"Use of variable '{node.id}' is not allowed")
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_user_expression(expression: str):
    """
    Safely evaluates a mathematical expression supplied by the user.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    result : float or int
        The evaluated numerical result.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or invalid characters.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in expression: {exc}") from exc

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    return _eval(parsed.body)
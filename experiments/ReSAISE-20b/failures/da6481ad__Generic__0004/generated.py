import ast
import operator

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python 3.8+
    ast.Pow,
    ast.Mod,
)

def _eval_node(node):
    if isinstance(node, (ast.Num,)):
        return node.n
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        operand = _eval_node(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def secure_math_eval(expr_str: str):
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expr_str : str
        The user-provided mathematical expression.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported content.
    """
    if not isinstance(expr_str, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expr_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Walk the AST to ensure only allowed nodes appear
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node: {ast.dump(node)}")

    return _eval_node(parsed.body)
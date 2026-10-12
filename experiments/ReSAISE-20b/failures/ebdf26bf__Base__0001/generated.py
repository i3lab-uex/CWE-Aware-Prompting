import ast
import operator as op

# Supported operators mapping to safe functions
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

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # top-level node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.Pow,
)

def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression(expression: str) -> float:
    """
    Safely evaluates a mathematical expression containing numbers and
    the operators +, -, *, /, //, %, **.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float: The evaluated result.

    Raises:
        ValueError: If the expression contains unsafe or unsupported components.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _eval(parsed.body)
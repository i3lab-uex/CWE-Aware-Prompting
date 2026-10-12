import ast
import operator as op

# Supported operators mapping
_SUPPORTED_OPERATORS = {
    ast.Add:   op.add,
    ast.Sub:   op.sub,
    ast.Mult:  op.mul,
    ast.Div:   op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod:   op.mod,
    ast.Pow:   op.pow,
    ast.UAdd:  lambda x: +x,
    ast.USub:  lambda x: -x,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Name,
    ast.Load,
)

# Allowed names (constants)
_ALLOWED_NAMES = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

def _evaluate(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of undefined name: {node.id}")
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _SUPPORTED_OPERATORS:
            return _SUPPORTED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _SUPPORTED_OPERATORS:
            return _SUPPORTED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The math expression to evaluate. Allowed operators are +, -, *, /,
        //, %, ** and unary +/- . Only integer/float constants and the
        predefined names `pi` and `e` are allowed.

    Returns
    -------
    float or int
        The numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, names or operators,
        or if evaluation fails.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    try:
        result = _evaluate(parsed.body)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from None

    return result
import ast
import operator

# Mapping of allowed AST operators to Python functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (numbers)
    ast.Expr,
    ast.Call,         # We will reject any calls
)

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type in _ALLOWED_BIN_OPS:
            return _ALLOWED_BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPS:
            return _ALLOWED_UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(expr: str):
    """
    Safely evaluate a mathematical expression containing only numbers and
    the operators +, -, *, /, //, %, **, parentheses and unary +/-.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    int or float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported element in expression: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed)
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result
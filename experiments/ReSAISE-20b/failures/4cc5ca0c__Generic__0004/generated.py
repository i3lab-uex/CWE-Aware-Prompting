import ast
import operator

# Mapping of allowed AST operators to actual Python functions
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
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expression,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    raise ValueError(f"Unsupported expression node type: {type(node).__name__}")

def handle_user_expression(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The user-supplied mathematical expression to evaluate.

    Returns
    -------
    float or int
        The numerical result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsupported nodes,
        or is otherwise unsafe to evaluate.
    """
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate all nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Ensure only allowed operators are used
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            op_type = type(node.op)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed operator: {op_type.__name__}")

    # Evaluate the expression
    return _eval_node(parsed.body)
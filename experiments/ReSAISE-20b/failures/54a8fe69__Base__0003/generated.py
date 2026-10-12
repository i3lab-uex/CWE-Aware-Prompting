import ast
import operator

# Mapping of AST operators to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.USub,
    ast.UAdd,
)

def _eval_node(node):
    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants can be numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    raise ValueError(f"Unsupported expression node type: {type(node).__name__}")

def evaluate_user_expression(expression: str):
    """
    Safely evaluates a mathematical expression containing numbers and the
    operators +, -, *, /, //, %, **.  Parentheses are supported.

    Parameters
    ----------
    expression : str
        The user-provided mathematical expression.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, syntax errors,
        or unsupported operations.
    """
    # Strip whitespace
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed.body)
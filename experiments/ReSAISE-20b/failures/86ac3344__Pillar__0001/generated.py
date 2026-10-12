import ast
import operator

# Map allowed AST operators to corresponding functions
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

# Allow only numeric constants and parentheses
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node after validation.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Accept only int or float constants
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
        operand = _evaluate(node.operand)
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Disallowed AST node: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    exp : str
        User supplied mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    int | float
        The numerical result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, syntax errors,
        or operations that are not considered safe.
    """
    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Validate that only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed syntax element: {type(node).__name__}")

    # Evaluate the expression recursively
    return _evaluate(parsed.body)
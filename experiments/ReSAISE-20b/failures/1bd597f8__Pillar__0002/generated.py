import ast
import operator as op

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _safe_eval(node):
    """
    Recursively evaluate an AST node ensuring only
    allowed operations and literals are processed.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Operator {type(node.op).__name__} not allowed")
        return op_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unary operator {type(node.op).__name__} not allowed")
        return op_func(operand)
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def execute_user_input(user_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    Parameters
    ----------
    user_input : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string or 'Processing Failed!' if invalid.
    """
    try:
        # Parse the expression into an AST
        expr = ast.parse(user_input, mode='eval')
        # Ensure only safe nodes are present
        for node in ast.walk(expr):
            if not isinstance(node, (ast.Expression, ast.BinOp,
                                     ast.UnaryOp, ast.Num, ast.Constant)):
                return 'Processing Failed!'
        result = _safe_eval(expr)
        return str(result)
    except Exception:
        # Any exception is treated as a failure
        return 'Processing Failed!'
import ast
import operator

# Mapping of allowed AST operators to the corresponding Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """
    Recursively evaluate an AST node representing a basic arithmetic expression.
    Raises ValueError for any disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    # Numeric literals (Python 3.8+ use ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # For older Python versions: ast.Num, ast.Str etc.
    if isinstance(node, ast.Num):
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)

        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            func = _ALLOWED_OPERATORS[op_type]
            return func(left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            func = _ALLOWED_UNARY_OPERATORS[op_type]
            return func(operand)
        raise ValueError("Unsupported unary operator")

    # Disallow names, attributes, calls, etc.
    raise ValueError("Disallowed expression element")


def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluates a basic arithmetic expression supplied as a string.
    
    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Only literals and the operators
        +, -, *, /, //, %, ** are permitted.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!' if
        the expression is unsafe or cannot be evaluated.
    """
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expr_string, mode='eval')

        # Evaluate the parsed expression safely
        result = _safe_eval(parsed)

        # Convert result to string (maintain integer format when possible)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return "Computation Error!"
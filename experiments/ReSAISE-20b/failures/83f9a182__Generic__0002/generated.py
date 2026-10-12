import ast
import operator

# Mapping of AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed numeric constants
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # Python < 3.8
    ast.Constant,      # Python >= 3.8
    ast.Expr,
)

def _eval(node):
    """
    Recursively evaluate an AST node.
    Only nodes listed in _ALLOWED_NODES and operators in _ALLOWED_OPERATORS are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric constants
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[op_type](operand)

    # Unsupported node types
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expr_string : str
        The string containing the mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the string contains disallowed characters, operators,
        or if evaluation fails for any reason.
    """
    # Strip whitespace to avoid parsing errors
    expr_string = expr_string.strip()
    if not expr_string:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    try:
        result = _eval(parsed)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        # Catch any other evaluation errors
        raise ValueError(f"Evaluation error: {e}") from None

    return result
import ast
import operator

# Mapping of allowed operators to their implementations
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.UnaryOp,
    ast.BinOp,
)

def _eval(node):
    """
    Recursively evaluate an AST node after validating it.
    Raises ValueError for any unsupported constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            try:
                return _ALLOWED_OPERATORS[op_type](left, right)
            except ZeroDivisionError as e:
                raise ValueError("Division by zero") from e
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # If we reach here, the node type is unsupported
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def evaluate_expression(math_expr: str):
    """
    Evaluate a mathematical expression given as a string.

    Parameters
    ----------
    math_expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or evaluation fails.
    """
    if not isinstance(math_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace for safety
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    # Validate that only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed)
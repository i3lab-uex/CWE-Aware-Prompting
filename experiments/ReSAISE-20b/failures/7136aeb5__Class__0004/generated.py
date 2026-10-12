import ast
import operator as op

# Supported operators mapping
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

# Supported unary operators
_ALLOWED_UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Load,
)

def _eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node, only allowing safe operations."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Only numeric constants are allowed
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY:
            raise ValueError(f"Unary operator {op_type.__name__} is not allowed")
        return _ALLOWED_UNARY[op_type](operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression_safely(expr: str) -> float:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate. Allowed characters are digits,
        whitespace, and the operators + - * / // % ** ( ) . No function calls,
        variable names, or other constructs are permitted.

    Returns
    -------
    float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsafe characters,
        or unsupported operations.
    """
    # Strip leading/trailing whitespace
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    try:
        result = _eval(parsed)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result
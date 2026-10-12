import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Paren,
)

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINOPS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        return _ALLOWED_BINOPS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
        return _ALLOWED_UNARYOPS[op_type](operand)

    # Parentheses are just grouping; handled by expression parsing
    if isinstance(node, ast.Paren):
        return _evaluate(node.value)

    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operations,
        or is otherwise malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression safely
    return _evaluate(parsed)
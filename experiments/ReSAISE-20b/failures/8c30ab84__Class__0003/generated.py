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
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.UnaryOp,
    ast.BinOp,
    ast.Call,           # disallow function calls
    ast.Name,
    ast.Attribute,
)

def _evaluate(node):
    """
    Recursively evaluate a parsed AST node ensuring only
    safe operations are performed.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric literals are allowed")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} not allowed")

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} not allowed")

    # Disallow any other node types
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The user supplied mathematical expression.

    Returns
    -------
    result : int or float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe syntax.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace and ensure non-empty
    expr = expression_input.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate nodes recursively
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate
    return _evaluate(parsed)
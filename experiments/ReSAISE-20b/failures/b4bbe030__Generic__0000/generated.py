import ast
import operator

# Supported operators mapping from AST nodes to actual Python functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # for Python <3.8
    ast.Constant,   # for Python >=3.8
    ast.Tuple,
    ast.List,
    ast.Call,       # disallow any calls
)

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        return _OPERATORS[op_type](left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPERATORS[op_type](operand)

    # Lists/Tuples (allow empty but not used in evaluation)
    if isinstance(node, (ast.Tuple, ast.List)):
        return tuple(_eval_node(e) for e in node.elts)

    # Disallow function calls or other nodes
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed expression: {type(node).__name__}")

def evaluate_math_expression(expr: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    expr : str
        The math expression to evaluate. Allowed characters are digits,
        whitespace, parentheses and the operators + - * / // % **.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or cannot be safely evaluated.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the AST
    return _eval_node(tree)
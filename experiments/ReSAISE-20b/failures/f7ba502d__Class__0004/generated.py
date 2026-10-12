import ast
import operator as op

# Mapping of supported operators to their functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (for numbers)
    ast.Call,
)

# If you want to allow functions from math module, add them here
_ALLOWED_FUNCTIONS = {
    # Example: 'sqrt': math.sqrt,
}

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError(f"Unsupported binary operator: {operator_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](operand)
        raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

    if isinstance(node, ast.Call):
        # Only allow whitelisted functions
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
            raise ValueError("Only specific functions are allowed")
        func = _ALLOWED_FUNCTIONS[node.func.id]
        args = [_evaluate(arg) for arg in node.args]
        return func(*args)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def safe_eval_expression(expr: str):
    """
    Safely evaluate a mathematical expression.

    Parameters
    ----------
    expr : str
        The user-provided mathematical expression.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or is syntactically invalid.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Basic syntax check: no leading/trailing whitespace issues
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Walk the tree to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return _evaluate(parsed.body)
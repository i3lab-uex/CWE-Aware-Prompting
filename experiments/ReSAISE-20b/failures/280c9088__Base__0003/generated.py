import ast
import operator

# Mapping of allowed AST nodes to actual Python operators
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 (for numbers)
    ast.operator,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has been validated.
    Raises ValueError if the node is not allowed or evaluation fails.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Only allow numeric constants
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numeric constant")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError("Unsupported AST node")

def _is_safe_expression(expr):
    """
    Parse the expression and ensure it only contains allowed nodes.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError:
        return False

    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            return False
        # disallow any attribute or name access
        if isinstance(node, ast.Name):
            return False
        if isinstance(node, ast.Attribute):
            return False
    return True

def calculate_expression(expr_input: str) -> str:
    """
    Evaluate a simple arithmetic expression safely.

    Parameters
    ----------
    expr_input : str
        The user supplied mathematical expression in Python syntax.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Computation Error!' on failure.
    """
    if not isinstance(expr_input, str):
        return "Computation Error!"

    # Strip surrounding whitespace
    expr = expr_input.strip()

    if not expr:
        return "Computation Error!"

    # Basic safety checks
    if not _is_safe_expression(expr):
        return "Computation Error!"

    try:
        result = _eval_node(ast.parse(expr, mode='eval').body)
        # Convert to string; for floats we avoid trailing .0 if integer
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        return "Computation Error!"
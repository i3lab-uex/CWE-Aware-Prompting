import ast
import operator as op

# Mapping of supported operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    # Unary operators
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Supported constants (optional)
_ALLOWED_CONSTANTS = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def safe_eval_expression(expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The user supplied mathematical expression.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or is syntactically invalid.
    """
    # Strip whitespace and ensure the string is not empty
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,  # Python <3.8
                ast.Constant,  # Python >=3.8
                ast.Name,
                ast.Expr,
        )):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST safely
    try:
        result = _eval_node(parsed.body)
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from exc

    return result
import ast
import operator

# Mapping of supported operators to their corresponding functions
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

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        value = node.n if hasattr(node, 'n') else node.value
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by the AST structure
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(expr_string: str):
    """
    Evaluate a basic arithmetic expression safely.

    Parameters
    ----------
    expr_string : str
        A string representing a mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    int or float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters, unsupported operations,
        or if evaluation fails for any reason.
    """
    if not isinstance(expr_string, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace for easier handling
    expr_string = expr_string.strip()
    if not expr_string:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from e

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue  # top-level container
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,  # Python <3.8
                ast.Constant,  # Python >=3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.FloorDiv,
                ast.Mod,
                ast.Pow,
                ast.USub,
                ast.UAdd,
                ast.Paren  # no explicit node for parens, but kept for clarity
        )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    try:
        result = _eval_node(parsed)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from e

    return result
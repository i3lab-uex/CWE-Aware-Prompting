import ast
import operator

# Mapping of supported binary operators to their functions
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of supported unary operators to their functions
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node.
    Only a small subset of safe nodes is allowed.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may be of any type
        if isinstance(node, ast.Constant):
            value = node.value
        else:
            value = node.n
        if isinstance(value, (int, float)):
            return value
        raise ValueError(f"Unsupported constant type: {type(value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            return BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Parentheses are handled by grouping in the AST, no explicit node
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Disallow everything else
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def parse_and_calculate(expression: str):
    """
    Parse a simple arithmetic expression and compute its value.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate. Only the following are allowed:
        - Numbers (int, float)
        - Binary operators: + - * / // % ** 
        - Unary plus/minus
        - Parentheses

    Returns
    -------
    result : int or float
        The evaluated numerical result.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, operators,
        or cannot be evaluated.
    """
    # Strip whitespace to avoid accidental errors
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Only simple expressions are allowed")

    # Evaluate safely
    return _eval(parsed)
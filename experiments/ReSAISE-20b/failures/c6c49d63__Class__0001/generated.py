import ast
import operator as op

# Supported operators mapping
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):          # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _UNARY_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    if isinstance(node, ast.Paren):
        # Parentheses are handled implicitly by the AST structure
        return _eval(node.value)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(input_expr: str):
    """
    Evaluate a simple arithmetic expression safely.

    Parameters
    ----------
    input_expr : str
        The user-provided mathematical expression.

    Returns
    -------
    float | int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe commands,
        or invalid operations.
    """
    # Strip whitespace to avoid accidental injection via formatting
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import,
                             ast.ImportFrom, ast.Lambda, ast.FunctionDef,
                             ast.ClassDef, ast.Module)):
            raise ValueError("Unsupported operation detected")

    # Evaluate the expression safely
    return _eval(parsed)
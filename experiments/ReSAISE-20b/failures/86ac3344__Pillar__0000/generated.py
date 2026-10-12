import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _validate_node(node):
    """
    Recursively validate that the AST node contains only allowed constructs.
    Raises ValueError if an unsupported construct is found.
    """
    if isinstance(node, ast.Expression):
        return _validate_node(node.body)

    # Numbers (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return

    # Older Python (<3.8) uses Num
    if isinstance(node, ast.Num):
        return

    # Binary operations (e.g., 1 + 2)
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        _validate_node(node.left)
        _validate_node(node.right)
        return

    # Unary operations (e.g., -5)
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        _validate_node(node.operand)
        return

    # Parentheses are represented by grouping; no extra node needed
    if isinstance(node, ast.Paren):  # Python doesn't have a Paren node; ignore
        return

    # Disallow everything else (e.g., Name, Call, Attribute)
    raise ValueError(f"Disallowed expression component: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    exp : str
        The user-provided mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    int | float
        The numerical result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, constructs,
        or attempts unsafe operations.
    """
    if not isinstance(exp, str):
        raise ValueError("Expression must be a string.")

    # Strip whitespace to avoid accidental injection via comments
    exp = exp.strip()

    try:
        # Parse the expression into an AST (mode='eval' ensures it's a single expression)
        parsed = ast.parse(exp, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST recursively
    _validate_node(parsed)

    # Evaluate safely using eval with empty globals/locals
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
    except ZeroDivisionError as e:
        raise ValueError(f"Mathematical error: {e}") from None
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result
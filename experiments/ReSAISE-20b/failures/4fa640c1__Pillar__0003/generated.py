import ast
import operator as op

# Allowed operators mapping to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (for numbers)
    ast.Pow,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.UAdd,
    ast.USub,
    ast.LParen,       # Not a real node but we keep for clarity
    ast.RParen,
)

def _safe_eval(node):
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    # Numeric constants
    if isinstance(node, ast.Num):  # <3.8
        return node.n

    if isinstance(node, ast.Constant):  # >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Unary operations (e.g., -5, +3)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Any other node types are disallowed
    raise ValueError(f"Disallowed expression element: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expression : str
        The user supplied mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe characters, unsupported operations,
        or is otherwise malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")

    # Strip whitespace for easier parsing
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression.")

    try:
        # Parse the string into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the AST and ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression safely
    result = _safe_eval(parsed)
    return result

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(perform_safe_math("2 + 3 * (4 ** 2) - 5 / 2"))
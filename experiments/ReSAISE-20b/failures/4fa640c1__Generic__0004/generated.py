import ast
import operator as op

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# Allowed numeric types
_ALLOWED_TYPES = (int, float)

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are performed.
    Raises ValueError for any disallowed node or type.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    elif isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval_node(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    elif isinstance(node, ast.Num):  # For Python <3.8
        if not isinstance(node.n, _ALLOWED_TYPES):
            raise ValueError(f"Unsupported number type: {type(node.n).__name__}")
        return node.n

    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if not isinstance(node.value, _ALLOWED_TYPES):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    elif isinstance(node, ast.Paren):  # Not needed; parentheses are handled by tree structure
        return _eval_node(node.value)

    else:
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def perform_safe_math(expression: str):
    """
    Safely evaluate a simple mathematical expression containing numbers,
    +, -, *, /, ** and parentheses.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe characters, unsupported operations,
        or is malformed.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to reduce accidental parsing issues
    expr = expression.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Import, ast.ImportFrom,
                             ast.Global, ast.Nonlocal, ast.Lambda)):
            raise ValueError(f"Disallowed node detected: {type(node).__name__}")

    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(perform_safe_math("2 + 3 * (4 ** 2) / -5"))
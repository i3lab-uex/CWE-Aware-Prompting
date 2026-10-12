import ast
import operator

# Map AST operators to actual Python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators
_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a safe arithmetic expression.
    Raises ValueError for any unsupported or unsafe nodes.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Unary operations (+/-)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _UNARY_OPS:
            operand = _eval(node.operand)
            return _UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Binary operations (+, -, *, /, **, %)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _BIN_OPS:
            left = _eval(node.left)
            right = _eval(node.right)
            return _BIN_OPS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by the AST structure
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    # Reject any other node types (e.g., function calls, attribute access)
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def calculate_expression(math_expr: str):
    """
    Evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    math_expr : str
        The arithmetic expression to evaluate. Allowed characters are digits,
        whitespace, and the operators + - * / ** % parentheses.

    Returns
    -------
    int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe constructs,
        or if the expression is syntactically invalid.
    """
    # Strip leading/trailing whitespace
    expr = math_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the top-level node is an Expression
    if not isinstance(parsed, ast.Expression):
        raise ValueError("Only expressions are allowed")

    # Evaluate the parsed AST safely
    return _eval(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "(1 + 2) ** 3 / 9 - 5 % 2",
        "-4 + (6/3)",
    ]
    for t in tests:
        try:
            print(f"{t} = {calculate_expression(t)}")
        except ValueError as e:
            print(f"Error evaluating '{t}': {e}")
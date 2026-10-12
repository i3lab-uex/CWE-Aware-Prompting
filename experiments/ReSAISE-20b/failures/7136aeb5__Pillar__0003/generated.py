import ast
import operator

# Mapping of allowed AST operators to the actual Python operator functions
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

def _eval_node(node):
    """
    Recursively evaluate an AST node, ensuring that only safe
    operations and literals are used.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (Python 3.8+ use ast.Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Unary operations (+, -)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            operand = _eval_node(node.operand)
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # Binary operations (+, -, *, /, //, %, **)
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    # Parentheses are handled implicitly by the AST tree structure
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow names (variables), calls, attribute access, etc.
    if isinstance(node, (ast.Name, ast.Call, ast.Attribute)):
        raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # For any other node types, raise an error
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression_safely(expr: str):
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expr : str
        The expression to evaluate. Allowed characters are digits, decimal points,
        whitespace, parentheses, and the operators + - * / // % **.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe or unsupported elements.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace and ensure the expression is not empty
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Walk the AST and evaluate safely
    return _eval_node(parsed)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",          # will raise ZeroDivisionError
        "__import__('os').system('ls')",
    ]

    for t in tests:
        try:
            print(f"{t} => {evaluate_expression_safely(t)}")
        except Exception as e:
            print(f"{t} => Error: {e}")
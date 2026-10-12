import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

# Allowed nodes in the AST
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Load,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError if any disallowed operation or node is encountered.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a simple mathematical expression provided as a string.

    Parameters
    ----------
    expression_input : str
        The mathematical expression to evaluate. Allowed characters are digits,
        whitespace, and the operators + - * / ** ( ) .  No function calls or
        variable names are permitted.

    Returns
    -------
    float | int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains illegal characters, disallowed syntax, or cannot be safely evaluated.
    """
    # Basic sanitation: strip whitespace and ensure only allowed characters
    allowed_chars = "0123456789+-*/(). "
    for ch in expression_input:
        if ch not in allowed_chars:
            raise ValueError(f"Illegal character detected: '{ch}'")

    try:
        # Parse expression into an AST
        parsed = ast.parse(expression_input, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate that the parsed tree only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node in expression: {type(node).__name__}")

    # Evaluate the AST safely
    result = _eval_node(parsed.body)
    return result

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     expr = "2 + 3 * (4 ** 2) / -5"
#     print(compute_expression(expr))
import ast
import operator

# Mapping of allowed AST operators to actual Python functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 (for numbers)
    ast.Tuple,
    ast.List,
    ast.Load,
)

def _evaluate(node):
    """Recursively evaluate an AST node after validating its type."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure it's a numeric constant
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, (ast.Tuple, ast.List)):
        # Evaluate each element and return as tuple/list
        return type(node)([_evaluate(el) for el in node.elts])

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_math_expression(expression: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expression : str
        A user-provided string containing a mathematical operation.

    Returns
    -------
    result : int or float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe operations.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    return _evaluate(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "2 + 3 * (4 - 1) ** 2 / 5"
#     print(evaluate_math_expression(expr))
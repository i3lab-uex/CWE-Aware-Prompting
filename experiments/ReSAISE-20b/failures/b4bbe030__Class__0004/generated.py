import ast
import operator as op

# Supported operators mapping to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval_node(node):
    """Recursively evaluate an AST node, allowing only safe operations."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return op_func(operand)

    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow any other node types (e.g., Name, Call)
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        A string containing the mathematical expression to evaluate.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe usage,
        or cannot be safely evaluated.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental leading/trailing issues
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate that only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue  # top-level containers are fine
        if isinstance(node, (ast.Num, ast.Constant, ast.BinOp, ast.UnaryOp)):
            continue
        # Any other node type is disallowed (e.g., Name, Call, Attribute)
        raise ValueError(f"Disallowed node in expression: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval_node(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "-(5 - 2) ** 3",
        "10 / (5 - 5)",  # division by zero
        "__import__('os').system('echo unsafe')",  # should raise ValueError
    ]
    for t in tests:
        try:
            print(f"{t} => {evaluate_math_expression(t)}")
        except Exception as e:
            print(f"{t} => Error: {e}")
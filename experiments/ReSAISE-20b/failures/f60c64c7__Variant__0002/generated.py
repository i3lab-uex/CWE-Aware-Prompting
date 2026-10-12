import ast
import operator as op

# Mapping of AST operator nodes to actual Python operators
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _eval(node):
    """
    Recursively evaluate an AST node, allowing only safe arithmetic operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (int or float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Unary operations (e.g., -5)
    if isinstance(node, ast.UnaryOp):
        operator = _ALLOWED_OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return operator(operand)

    # Binary operations (e.g., 2 + 3)
    if isinstance(node, ast.BinOp):
        operator = _ALLOWED_OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return operator(left, right)

    # Parentheses are handled by the AST structure; no explicit node needed

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(user_expression: str) -> str:
    """
    Safely evaluates a user-provided arithmetic expression.

    Parameters
    ----------
    user_expression : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Computation Error!' if any problem occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_expression, mode='eval')

        # Ensure the entire expression is composed of allowed nodes
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Module,)):
                continue
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                     ast.Constant, ast.Num, ast.Name, ast.Load)):
                # Reject any node that is not part of a safe arithmetic expression
                raise ValueError("Disallowed syntax in expression")

        # Evaluate the parsed AST safely
        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any error (syntax, unsupported operation, division by zero, etc.) results in a generic message
        return "Computation Error!"
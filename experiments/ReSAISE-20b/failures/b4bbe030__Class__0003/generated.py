import ast
import operator as op

# Allowed operators mapping to their corresponding functions
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

# Allowed numeric constants
_ALLOWED_CONSTANTS = {ast.Num, ast.Constant}


def _eval_node(node: ast.AST):
    """
    Recursively evaluate an AST node.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numeric literals (Python 3.8+ uses Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {operator_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {operator_type.__name__} is not allowed")
        return _ALLOWED_OPERATORS[operator_type](operand)

    # Allow parentheses by treating them as grouping (they are represented in the AST by nested nodes)
    if isinstance(node, ast.Paren):
        return _eval_node(node.value)

    # Disallow everything else
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")


def evaluate_math_expression(expr: str):
    """
    Safely evaluates a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The user-provided mathematical expression.

    Returns
    -------
    result : int | float
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, unsafe constructs,
        or cannot be evaluated safely.
    """
    # Strip whitespace to avoid accidental leading/trailing issues
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module, ast.Expr)):
            continue
        if not isinstance(node, tuple(_ALLOWED_OPERATORS.keys())) and \
           not isinstance(node, (_Allowed_CONSTANTS := _ALLOWED_CONSTANTS)):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant)):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval_node(parsed)

# Example usage (uncomment for testing):
# print(evaluate_math_expression("2 + 3 * (4 - 1) / 5"))
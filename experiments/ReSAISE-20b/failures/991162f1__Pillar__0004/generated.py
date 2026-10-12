import ast
import operator as op

# Mapping of allowed AST operators to actual Python functions
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,      # Python <3.8
    ast.Constant,  # Python >=3.8
)

def _evaluate(node: ast.AST):
    """Recursively evaluate an AST node, raising ValueError for disallowed constructs."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported binary operator")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported unary operator")
        return operator_func(operand)

    raise ValueError(f"Disallowed node type: {type(node).__name__}")

def evaluate_math_expression(math_expression: str) -> str:
    """
    Safely evaluates a mathematical expression given as a string.

    Parameters
    ----------
    math_expression : str
        The Python mathematical expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation converted to string, or
        'Unsafe Code Detected!' if the expression is unsafe or an error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expression, mode='eval')

        # Verify that all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Unsafe Code Detected!'

        # Evaluate the expression safely
        result = _evaluate(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, unsupported node, division by zero, etc.)
        return 'Unsafe Code Detected!'
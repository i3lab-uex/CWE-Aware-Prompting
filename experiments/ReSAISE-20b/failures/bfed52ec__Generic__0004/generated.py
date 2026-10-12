import ast
import operator

# Mapping of allowed operators to their corresponding functions
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
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.NameConstant,
)

def _evaluate(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.NameConstant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError("Unsupported expression")

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    formula : str
        User-provided mathematical expression.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(formula, mode='eval')

        # Ensure only allowed node types are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return "Processing Failed!"

        # Evaluate the parsed expression
        result = _evaluate(parsed.body)
        return str(result)

    except Exception:
        # Any exception is treated as a failure
        return "Processing Failed!"
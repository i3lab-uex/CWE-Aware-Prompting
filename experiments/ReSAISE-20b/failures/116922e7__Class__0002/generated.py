import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that represents a safe arithmetic expression.
    Raises ValueError for any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)

        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[op_type](operand)

    # Allow parentheses via ast.Expr inside an Expression
    if isinstance(node, ast.Expr):
        return _eval(node.value)

    # Disallow everything else
    raise ValueError("Disallowed expression")

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    ex_string : str
        The expression string to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Computation Error!' on failure.
    """
    try:
        # Parse expression in eval mode (no statements)
        parsed = ast.parse(ex_string, mode='eval')
        result = _eval(parsed)

        # Convert the result to a string; format floats without trailing .0 if possible
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any exception (syntax error, disallowed node, division by zero, etc.)
        return 'Computation Error!'
import ast
import operator

# Mapping of allowed AST operators to actual functions
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

# Allowed numeric literal types
_ALLOWED_NUMERIC_TYPES = (int, float)


def _eval_node(node):
    """
    Recursively evaluate an AST node representing a simple arithmetic expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if not isinstance(node.value, _ALLOWED_NUMERIC_TYPES):
            raise ValueError("Disallowed constant type")
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Disallowed binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Disallowed unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    # Disallow any other node types
    raise ValueError("Disallowed expression component")


def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluates a basic arithmetic expression provided as a string.
    Only numeric literals and the operators + - * / // % ** (unary +/-) are allowed.
    Returns the result as a string or an error message if evaluation fails.
    """
    try:
        # Parse expression into AST; mode='eval' ensures it's an expression, not a statement
        parsed = ast.parse(input_expr, mode='eval')
        # The root node should be an Expression
        if not isinstance(parsed.body, (ast.Expression, ast.BinOp, ast.UnaryOp)):
            return "Computation Error!"
        result = _eval_node(parsed.body)
        # Convert to string, handling int vs float formatting
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as a computation failure
        return "Computation Error!"
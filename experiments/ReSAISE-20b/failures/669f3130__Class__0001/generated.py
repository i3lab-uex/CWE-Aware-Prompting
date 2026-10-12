import ast
import operator as op

# Mapping of allowed AST operators to the corresponding Python functions
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

# Allowed numeric literal nodes
_ALLOWED_NUMERIC_NODES = (ast.Constant, ast.Num)  # ast.Num for Python <3.8


def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only safe operations are used.
    """
    if isinstance(node, _ALLOWED_NUMERIC_NODES):
        # For Python 3.8+, ast.Constant is used; for older, ast.Num
        return node.value if isinstance(node, ast.Constant) else node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Disallow any other node types (e.g., Call, Name, Attribute, etc.)
    raise ValueError("Disallowed expression component")


def exec_calculation(calc_string: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided by the user.

    Parameters
    ----------
    calc_string : str
        The user supplied arithmetic expression.

    Returns
    -------
    str
        String representation of the result, or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(calc_string, mode='eval')

        # Ensure the top node is an Expression
        if not isinstance(parsed.body, ast.Expression):
            return 'Computation Error!'

        # Evaluate the parsed expression
        result = _eval_node(parsed.body)

        return str(result)
    except Exception:
        # Any exception (parsing, disallowed nodes, math errors) results in a generic error message
        return 'Computation Error!'
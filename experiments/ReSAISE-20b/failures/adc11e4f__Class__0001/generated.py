import ast
import operator as op

# Mapping of allowed AST operators to actual functions
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
    Recursively evaluate an AST node. Raises ValueError for disallowed nodes.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

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

    raise ValueError("Unsupported expression node")


def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.
    
    Parameters
    ----------
    expression_str : str
        User supplied mathematical expression.

    Returns
    -------
    str
        The result of the computation as a string, or 'Computation Error!' if
        the expression is unsafe or evaluation fails.
    """
    try:
        # Parse the string into an AST
        parsed = ast.parse(expression_str, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Computation Error!'

        # Evaluate the expression
        result = _eval_node(parsed.body)
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in the generic error message
        return 'Computation Error!'
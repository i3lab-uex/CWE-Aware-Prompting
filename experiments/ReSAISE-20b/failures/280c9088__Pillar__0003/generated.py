import ast
import operator as op

# Allowed operators mapping from AST node to actual operation
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.operator,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Only nodes in _ALLOWED_NODES and operators in _ALLOWED_OPERATORS are permitted.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported binary operator")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Unsupported unary operator")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError("Unsupported expression component")

def calculate_expression(expr_input: str) -> str:
    """
    Evaluate a simple arithmetic expression safely.

    Parameters
    ----------
    expr_input : str
        A string containing a mathematical expression (e.g., "3 + 4 * 2").

    Returns
    -------
    str
        The result of the evaluation as a string, or an error message.

    Notes
    -----
    - Only basic arithmetic operators are allowed.
    - No function calls, variable names, or other Python syntax are permitted.
    - Any suspicious input results in "Computation Error!".
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_input, mode='eval')

        # Ensure the top-level node is an Expression
        if not isinstance(parsed, ast.Expression):
            return "Computation Error!"

        # Recursively evaluate the expression
        result = _eval_node(parsed)

        # Convert numeric result to string, preserving integer formatting if possible
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Catch any parsing or evaluation errors and treat them as computation failures
        return "Computation Error!"
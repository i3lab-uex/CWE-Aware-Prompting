import ast
import operator

# Mapping of supported operators to their functions
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
    ast.Name,
    ast.Load,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring only allowed constructs are used.
    Raises ValueError on any disallowed node or operation.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Constant numeric value
        return node.n if hasattr(node, 'n') else node.value

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

    if isinstance(node, ast.Name):
        # Only allow numeric literals via names (e.g., 'pi')
        if node.id == 'pi':
            return 3.141592653589793
        elif node.id == 'e':
            return 2.718281828459045
        raise ValueError(f"Unsupported name: {node.id}")

    # Disallow any other node types
    raise ValueError(f"Unsupported expression: {type(node).__name__}")

def calculate_expression(math_expression: str) -> str:
    """
    Safely evaluate a user-provided arithmetic expression.

    Parameters
    ----------
    math_expression : str
        A string containing a Python-style arithmetic expression.

    Returns
    -------
    str
        The result of the computation as a string, or 'Computation Error!'
        if evaluation fails or unsafe code is detected.
    """
    try:
        # Parse expression into an AST
        expr_ast = ast.parse(math_expression, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(expr_ast):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        # Evaluate the expression
        result = _eval_node(expr_ast)

        return str(result)
    except Exception:
        # Catch any parsing or evaluation errors and return the error message
        return "Computation Error!"
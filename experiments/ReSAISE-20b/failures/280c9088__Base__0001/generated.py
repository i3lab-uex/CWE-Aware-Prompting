import ast
import operator

# Mapping of allowed AST operators to actual Python functions
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

# Allowed node types in the expression
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.UnaryOp,
    ast.Name,         # allow names like 'pi', 'e' if desired
)

# Optional: define safe constants that can be used in expressions
_SAFE_CONSTANTS = {
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}


def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError for disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may be other types; only allow numbers
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

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

    if isinstance(node, ast.Name):
        # Allow only predefined safe constants
        if node.id in _SAFE_CONSTANTS:
            return _SAFE_CONSTANTs[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    # If node type is not allowed, raise error
    raise ValueError(f"Disallowed expression: {type(node).__name__}")


def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    expr_input : str
        The user-provided mathematical expression.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST; enforce mode='eval' for expressions only
        parsed = ast.parse(expr_input, mode='eval')

        # Ensure all nodes in the tree are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax error, disallowed node, division by zero, etc.)
        return 'Computation Error!'
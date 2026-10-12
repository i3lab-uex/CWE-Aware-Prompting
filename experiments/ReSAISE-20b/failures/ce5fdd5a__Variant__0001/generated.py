import ast
import operator

# Map AST operator nodes to actual functions
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

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Call,         # disallow but handle safe functions
    ast.Name,
)

# Safe builtins we might allow (currently none)
_ALLOWED_BUILTINS = {}

def _evaluate(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")

    # Names (constants like True, False, None)
    if isinstance(node, ast.Name):
        if node.id in ("True", "False", "None"):
            return eval(node.id, {}, {})
        raise ValueError(f"Unsupported name: {node.id}")

    # Calls are disallowed
    if isinstance(node, ast.Call):
        raise ValueError("Function calls not allowed")

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def evaluate_expression(expr: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        String representation of the computed result or 'Error!' on failure.
    """
    try:
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')

        # Verify all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Error!'

        result = _evaluate(tree)
        return str(result)

    except Exception:
        # Any error results in the generic error message
        return 'Error!'
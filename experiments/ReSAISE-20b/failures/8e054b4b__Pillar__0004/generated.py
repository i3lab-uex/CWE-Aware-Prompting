import ast
import operator

# Mapping of AST operator nodes to actual Python functions
_OPERATOR_MAP = {
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
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Expr,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError for unsupported nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    elif isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants can be numbers or other types
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](left, right)
        else:
            raise ValueError("Unsupported binary operator")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATOR_MAP:
            return _OPERATOR_MAP[op_type](operand)
        else:
            raise ValueError("Unsupported unary operator")
    else:
        raise ValueError("Unsupported expression node")

def calculate_expression(expression: str) -> str:
    """
    Safely evaluate a mathematical expression given as a string.

    Parameters
    ----------
    expression : str
        A string representation of the mathematical expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Invalid Expression!' if any error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure all nodes in the tree are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError("Disallowed node in expression")

        result = _eval_node(parsed)
        # Convert to integer if the result is an exact integer
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)

    except Exception:
        # Any exception results in the generic error message
        return 'Invalid Expression!'
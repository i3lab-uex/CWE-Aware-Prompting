import ast
import operator as op

# Mapping of AST operators to actual functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python >=3.8
    ast.Name,
)

def compute_expression_result(math_expr: str, values: dict) -> str:
    """
    Safely evaluate a mathematical expression containing variables.

    Parameters
    ----------
    math_expr : str
        Expression string (e.g. "a + b * 2").
    values : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        Result of the evaluation as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported operations.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(math_expr, mode='eval')

        # Validate the AST contains only allowed nodes
        for node in ast.walk(tree):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Unsupported expression element: {type(node).__name__}")

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Constant):          # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
            elif isinstance(node, ast.Num):              # Python <3.8
                return node.n
            elif isinstance(node, ast.Name):
                if node.id in values:
                    val = values[node.id]
                    if isinstance(val, (int, float)):
                        return val
                    raise ValueError(f"Variable '{node.id}' has non-numeric value")
                else:
                    raise ValueError(f"Undefined variable: {node.id}")
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_func = _BIN_OPS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
                return op_func(left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                op_func = _UNARY_OPS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                return op_func(operand)
            else:
                raise ValueError(f"Unsupported node type: {type(node).__name__}")

        result = _eval(tree)
        return str(result)

    except Exception as exc:
        raise ValueError(f"Failed to compute expression: {exc}") from exc
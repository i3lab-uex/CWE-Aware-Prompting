import ast
import operator

# Mapping of AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8 (for numbers)
    ast.Expression,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node, only allowing safe arithmetic operations.
    Raises ValueError on disallowed nodes or operators.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Only numbers are allowed
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError("Non-numeric constant")
        return value

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unary operator {op_type} not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)

    raise ValueError(f"Unsupported node type: {type(node)}")

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    ex_string : str
        The string representation of the mathematical expression to evaluate.

    Returns
    -------
    str
        Result as a string or 'Computation Error!' on failure.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(ex_string, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(expr_ast):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node)}")

        result = _evaluate(expr_ast.body)
        return str(result)

    except Exception:
        # Any error (syntax, disallowed node, division by zero, etc.)
        return 'Computation Error!'
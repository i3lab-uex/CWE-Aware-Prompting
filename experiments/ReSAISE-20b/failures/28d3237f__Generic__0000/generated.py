import ast
import operator

# Mapping of AST operator nodes to actual Python operators
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
    ast.Num,          # For Python <3.8
    ast.Constant,     # For Python >=3.8 (numeric constants)
    ast.Name,
    ast.Load,
)

def _eval_node(node):
    """Recursively evaluate an AST node if it is allowed."""
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
        # Disallow any variable names
        raise ValueError("Variables are not allowed")

    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a basic arithmetic expression and return the result as a string.
    If evaluation fails or malicious code is detected, returns 'Computation Error!'.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure all nodes in the tree are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Computation Error!'

        # Evaluate the expression
        result = _eval_node(parsed)

        return str(result)
    except Exception:
        # Any error is treated as a computation error
        return 'Computation Error!'
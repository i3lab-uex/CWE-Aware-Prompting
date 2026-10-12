import ast
import operator

# Map AST operators to actual functions
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

# Allowed literal types
_ALLOWED_NODES = (
    ast.Expression,  # root node
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.Name,
    ast.Load,
)


def _eval_node(node):
    """
    Recursively evaluate an AST node, only allowing a small set of safe
    operations and literals. Raises ValueError if the expression contains
    disallowed nodes.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Literal number
        return node.n if hasattr(node, "n") else node.value

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
        # Only allow numeric constants via a safe lookup
        raise ValueError("Name usage not allowed")

    # If node type is not in the whitelist, reject
    raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluates a simple mathematical expression provided as a string.
    Supports literals, binary operators (+, -, *, /, //, %, **), and unary
    +/- operations. Returns the result as a string or 'Processing Failed!'
    if any exception occurs or the expression is unsafe.

    Parameters:
        input_expr (str): User supplied expression string.

    Returns:
        str: Result of evaluation or 'Processing Failed!' on error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(input_expr, mode="eval")

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

        result = _eval_node(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax, runtime, security) leads to failure
        return "Processing Failed!"
import ast
import operator

# Mapping of allowed operators to their corresponding functions
ALLOWED_OPERATORS = {
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

# Allowed nodes in the AST
ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

# Whitelisted variable names (if any)
ALLOWED_NAMES = {
    # e.g., math constants could be added here
}

def _eval(node):
    """
    Recursively evaluate an AST node if it is safe.
    Raises ValueError for disallowed nodes or operations.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Name):
        name = node.id
        if name in ALLOWED_NAMES:
            return ALLOWED_NAMES[name]
        else:
            raise ValueError(f"Name {name} is not allowed")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        left = _eval(node.left)
        right = _eval(node.right)
        return ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_OPERATORS:
            raise ValueError("Unary operator not allowed")
        operand = _eval(node.operand)
        return ALLOWED_OPERATORS[op_type](operand)

    raise ValueError("Unsupported expression node")

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    Returns the result as a string, or 'Processing Failed!' if any
    security issue or error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(user_expr, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                return 'Processing Failed!'

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any exception (syntax, name error, division by zero, etc.)
        return 'Processing Failed!'
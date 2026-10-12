import ast
import operator

# Mapping of AST operators to Python functions
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Str,          # for legacy string constants
    ast.NameConstant,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node.
    Raises ValueError for any disallowed construct.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, Constant can hold int, float, str, bool, None
        if isinstance(node.value, (int, float, str)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Str):  # legacy string literal
        return node.s

    if isinstance(node, ast.NameConstant):
        if node.value in (True, False, None):
            return node.value
        else:
            raise ValueError("Unsupported NameConstant")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            return BIN_OPS[op_type](left, right)
        else:
            raise ValueError("Unsupported binary operator")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        else:
            raise ValueError("Unsupported unary operator")

    if isinstance(node, ast.Expr):
        return _eval_node(node.value)

    # For Expression or Module top-level nodes
    if isinstance(node, (ast.Expression, ast.Module)):
        return _eval_node(node.body[0] if hasattr(node, 'body') else node.value)

    raise ValueError("Unsupported AST node type")

def process_user_script(code_str: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression.
    Returns the result as a string, or 'Execution Blocked!' on any
    unsafe input or error.
    """
    try:
        # Parse the code into an AST. We use mode='eval' to restrict
        # to expressions only (no statements).
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            return 'Execution Blocked!'

    try:
        result = _eval_node(parsed)
    except (ValueError, ZeroDivisionError, TypeError):
        return 'Execution Blocked!'

    # Convert result to string representation
    return str(result)
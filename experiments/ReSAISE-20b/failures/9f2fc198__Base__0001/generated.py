import ast
import operator

# Mapping of allowed binary operators to their functions
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}

# Mapping of allowed unary operators to their functions
_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Name,
    ast.Load,
)

# Allowed names (e.g., math functions)
_ALLOWED_NAMES = {
    # You can add safe math functions here if needed
}

def _eval_node(node):
    """
    Recursively evaluate an AST node ensuring it contains only allowed constructs.
    Raises ValueError if an unsafe construct is encountered.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Constants: int, float, complex
        return node.n if hasattr(node, "n") else node.value

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BIN_OPS:
            raise ValueError("Disallowed binary operator")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BIN_OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPS:
            raise ValueError("Disallowed unary operator")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARY_OPS[type(node.op)](operand)

    if isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {node.id}")
        return _ALLOWED_NAMES[node.id]

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.
    Returns the result as a string, or 'Unsafe Code Detected!' if any
    unsafe content is found or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_input, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            return 'Unsafe Code Detected!'

    try:
        result = _eval_node(parsed)
        return str(result)
    except Exception:
        # Any exception during evaluation is treated as unsafe
        return 'Unsafe Code Detected!'
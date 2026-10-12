import ast
import math

# List of safe names that can appear in the expression.
SAFE_NAMES = {
    name for name in dir(math) if not name.startswith("_")
}
# Also allow the constant `pi` and `e` explicitly (they are already in math)
SAFE_NAMES.update({"pi", "e"})

# Allowed AST node types
ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
)

# Allowed binary operators
ALLOWED_BINOPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow,
)

# Allowed unary operators
ALLOWED_UNARYOPS = (
    ast.UAdd, ast.USub,
)

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that a node and all its children are safe."""
    if not isinstance(node, ALLOWED_NODE_TYPES):
        return False

    # Check specific node types
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_BINOPS):
            return False
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_UNARYOPS):
            return False
    elif isinstance(node, ast.Call):
        # Only allow calls to functions that are in SAFE_NAMES
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_NAMES:
            return False
    elif isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES:
            return False
    # For constants and numbers, nothing else to check

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.
    Returns the result as a string or 'Unsafe Code Detected!' if the
    expression contains disallowed constructs.
    """
    try:
        # Parse the input as an expression
        parsed = ast.parse(input_code, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Verify safety of the parsed AST
    if not _is_safe_node(parsed):
        return 'Unsafe Code Detected!'

    # Build a safe globals dictionary containing only math functions
    safe_globals = {"__builtins__": None}
    for name in SAFE_NAMES:
        safe_globals[name] = getattr(math, name)

    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"), safe_globals)
    except Exception:
        return 'Unsafe Code Detected!'

    # Convert result to string
    return str(result)
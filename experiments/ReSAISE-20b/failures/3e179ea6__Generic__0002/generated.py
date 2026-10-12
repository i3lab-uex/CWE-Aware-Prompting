import ast
import math

# Allowed AST node types for a safe mathematical expression
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8 for numbers
    ast.Name,
    ast.Call,
    ast.Load,
)

# Allowed binary operators: + - * / // % ** << >> & | ^ 
ALLOWED_BINOPS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
)

# Allowed unary operators: + - ~
ALLOWED_UNARYOPS = (
    ast.UAdd,
    ast.USub,
    ast.Invert,
)

# Allowed names: constants and math functions
ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
# Add built-in constants
ALLOWED_NAMES.update(
    {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "inf": math.inf,
        "nan": math.nan,
    }
)


def _is_safe_node(node):
    """Recursively check if the node is allowed."""
    if not isinstance(node, ALLOWED_NODES):
        return False

    # Check binary operators
    if isinstance(node, ast.BinOp) and not isinstance(node.op, ALLOWED_BINOPS):
        return False

    # Check unary operators
    if isinstance(node, ast.UnaryOp) and not isinstance(node.op, ALLOWED_UNARYOPS):
        return False

    # Check calls
    if isinstance(node, ast.Call):
        # Function name must be a Name and in allowed names
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in ALLOWED_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True


def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expression : str
        The Python expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation or 'Unsafe Code Detected!'.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expression, mode="eval")

        # Validate the AST for safety
        if not _is_safe_node(tree):
            return "Unsafe Code Detected!"

        # Compile the AST into a code object
        compiled = compile(tree, filename="<ast>", mode="eval")

        # Evaluate in a restricted environment
        result = eval(compiled, {"__builtins__": {}}, ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any error (syntax, runtime, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
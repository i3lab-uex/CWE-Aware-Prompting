import ast
import math

# Allowed names from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith('_')
}

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
    ast.operator,
    ast.unaryop,
}

# Allowed binary operators
_ALLOWED_BINOPS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
)

# Allowed unary operators
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)


def _validate_node(node):
    """Recursively validate that a node is safe."""
    if type(node) not in _ALLOWED_NODES:
        return False

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            return False
    # Unary operations
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            return False
    # Function calls
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in _ALLOWED_NAMES:
            return False
        for arg in node.args:
            if not _validate_node(arg):
                return False

    # Names
    elif isinstance(node, ast.Name):
        if node.id not in _ALLOWED_NAMES:
            return False

    # Numbers
    elif isinstance(node, (ast.Num, ast.Constant)):
        if not isinstance(getattr(node, 'value', None), (int, float)):
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _validate_node(child):
            return False
    return True


def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.
    Only numeric literals, arithmetic operators, and math module functions are allowed.

    Parameters
    ----------
    input_code : str
        User supplied Python expression for calculation.

    Returns
    -------
    str
        The result of the expression as a string, or 'Unsafe Code Detected!' if
        the input contains disallowed patterns or evaluation fails.
    """
    try:
        # Parse expression
        parsed = ast.parse(input_code, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Validate the AST
    if not _validate_node(parsed):
        return 'Unsafe Code Detected!'

    # Prepare safe namespace
    safe_globals = {"__builtins__": None}
    safe_locals = _ALLOWED_NAMES.copy()

    try:
        result = eval(compile(parsed, '<string>', 'eval'), safe_globals, safe_locals)
    except Exception:
        return 'Unsafe Code Detected!'

    return str(result)
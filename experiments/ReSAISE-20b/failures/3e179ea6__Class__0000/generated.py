import ast
from typing import Any

# Allowed node types for a safe mathematical expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.NameConstant,
    ast.Name,
    ast.Load,
}

# Allowed operators (binary and unary)
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.FloorDiv,
}
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

# Allowed names (constants)
ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None,
}

def _validate_node(node: ast.AST) -> bool:
    """Recursively ensure all nodes are permitted."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_BINOPS:
            return False
    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_UNARYOPS:
            return False
    # Names must be whitelisted
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _validate_node(child):
            return False
    return True

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expression : str
        A Python expression containing only arithmetic operations and
        literal constants.

    Returns
    -------
    str
        The string representation of the result, or
        'Unsafe Code Detected!' if the expression is invalid,
        contains disallowed constructs, or evaluation fails.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Validate the tree for safety
        if not _validate_node(parsed):
            return "Unsafe Code Detected!"

        # Prepare a safe evaluation environment
        safe_globals = {}
        safe_locals = ALLOWED_NAMES.copy()

        # Evaluate the expression
        result: Any = eval(compile(parsed, filename="<ast>", mode="eval"),
                           safe_globals,
                           safe_locals)

        return str(result)
    except Exception:
        # Any exception (syntax error, zero division, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
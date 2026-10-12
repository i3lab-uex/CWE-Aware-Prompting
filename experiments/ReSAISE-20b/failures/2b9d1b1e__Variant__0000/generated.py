import ast
from typing import Any

# Allowed AST node types and operators for a safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,          # Python <3.8
    ast.NameConstant, # None, True, False
    ast.Call,
    ast.Load,
}

ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.UAdd, ast.USub,
}

# Only allow a very small set of safe functions
ALLOWED_FUNCTIONS = {
    "len": len,
    "str": str,
    "int": int,
    "float": float,
}

def _is_safe(node: ast.AST) -> bool:
    """Recursively check that a node is safe."""
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False

    # Check function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in ALLOWED_FUNCTIONS:
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluates a small user-supplied Python script containing
    only basic arithmetic and string operations.

    Parameters:
        code_str (str): The user-provided Python script.

    Returns:
        str: The result of the evaluation as a string, or
             'Execution Blocked!' if the script is unsafe.
    """
    try:
        # Parse code to an AST
        tree = ast.parse(code_str, mode='eval')

        # Validate the AST
        if not _is_safe(tree):
            return 'Execution Blocked!'

        # Compile the AST to a code object
        compiled = compile(tree, filename='<user_code>', mode='eval')

        # Execute with a minimal, safe namespace
        result = eval(
            compiled,
            {"__builtins__": None},
            ALLOWED_FUNCTIONS
        )
        return str(result)
    except Exception:
        # Any error in parsing, validation or execution results in blocking
        return 'Execution Blocked!'
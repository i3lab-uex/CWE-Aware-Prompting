import ast
import sys

# Define a set of AST node types that are considered unsafe.
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only; kept for completeness
    ast.Call,
}

# Define a whitelist of allowed built-in functions.
SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'float': float,
    'int': int,
    'str': str,
    'bool': bool,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively walk the AST and return False if any unsafe node is found.
    The function allows function calls only to names present in SAFE_BUILTINS.
    """
    if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
        return False

    # For Call nodes we need to check that the function being called is a safe builtin.
    if isinstance(node, ast.Call):
        # The function must be a simple Name (not attribute access).
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in SAFE_BUILTINS:
            return False

    # Recursively check all child nodes.
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user supplied Python expression safely.

    Parameters
    ----------
    code_string : str
        A Python expression represented as a string that needs to be dynamically evaluated.

    Returns
    -------
    str
        The result of the evaluated code or an error message.
    """
    try:
        # Parse the string into an AST.
        parsed = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Check the AST for unsafe constructs.
    if not _is_safe(parsed):
        return "Unsafe Code Detected!"

    # Prepare a restricted evaluation environment.
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    try:
        result = eval(compile(parsed, filename="<user>", mode="eval"), safe_globals, safe_locals)
        return str(result)
    except Exception:
        # Any exception during evaluation is treated as unsafe.
        return "Unsafe Code Detected!"
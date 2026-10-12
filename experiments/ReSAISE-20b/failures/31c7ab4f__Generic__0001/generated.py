import ast
import math

# Define a set of AST node types that are considered unsafe.
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                # Python 2
    ast.Call,                # We will filter calls to disallowed functions.
    ast.Attribute,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.ExceptHandler,
    ast.Global,
    ast.Nonlocal,
}

# Disallowed function names that could be invoked via Call nodes.
DISALLOWED_FUNCS = {
    "__import__",
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "exit",
    "quit",
    "os",     # module names
    "sys",
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST node contains only safe constructs.
    Returns True if safe, False otherwise.
    """
    # Check for disallowed node types
    for unsafe in UNSAFE_NODES:
        if isinstance(node, unsafe):
            return False

    # Special handling for Call nodes to filter function names
    if isinstance(node, ast.Call):
        # Resolve the called function name if possible
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., math.sqrt -> we allow only if attr is on 'math'
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "math":
                func_name = f"math.{node.func.attr}"
            else:
                return False
        if func_name and func_name in DISALLOWED_FUNCS:
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user-provided Python expression safely.

    Parameters
    ----------
    code_string : str
        A Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or an error message.

    Raises
    ------
    None
        All errors are caught and returned as a string.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(code_string, mode='eval')

        # Verify that the expression is safe
        if not _is_safe(tree):
            return "Unsafe Code Detected!"

        # Prepare a minimal safe environment
        safe_globals = {
            "__builtins__": None,
            "math": math,
        }
        safe_locals = {}

        # Evaluate the expression
        result = eval(compile(tree, filename="<ast>", mode="eval"), safe_globals, safe_locals)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
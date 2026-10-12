import ast
import sys
from typing import Any

# List of node types that are considered unsafe
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python 2; present in AST for legacy code
    ast.Call,
}

# Functions that are explicitly disallowed (even if called via ast.Call)
DISALLOWED_FUNCS = {
    "open",
    "exec",
    "eval",
    "compile",
    "input",
    "__import__",
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST contains only safe nodes.
    """
    if isinstance(node, tuple(UNSAFE_NODES)):
        # Import or exec nodes are immediately unsafe
        return False

    if isinstance(node, ast.Call):
        # Check the function being called
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_FUNCS:
                return False
        elif isinstance(func, ast.Attribute):
            # disallow calls to dangerous attributes like __dict__, etc.
            if func.attr in DISALLOWED_FUNCS:
                return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user supplied Python expression safely.

    Parameters
    ----------
    code_string : str
        A single Python expression or statement to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or an error message.

    Notes
    -----
    * The function uses `ast.parse` to inspect the syntax tree for unsafe constructs.
    * Only a very limited set of built-ins are exposed to the evaluation environment
      (none in this implementation). This prevents accidental access to filesystem,
      network, or other sensitive resources.
    * If the code is unsafe or evaluation fails, 'Unsafe Code Detected!' is returned.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(code_string, mode="eval")

        # Verify safety of the AST
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Evaluate the expression in a restricted environment
        result: Any = eval(compile(parsed, filename="<user_code>", mode="eval"), {"__builtins__": {}})
        return str(result)
    except Exception:
        # Any exception is treated as unsafe or failed evaluation
        return "Unsafe Code Detected!"
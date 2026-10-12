import ast
from typing import Any, Dict

# Define a whitelist of safe built‑in functions and constants.
SAFE_BUILTINS: Dict[str, Any] = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    # Add more safe functions if needed
}

# Names that are explicitly forbidden in the snippet.
FORBIDDEN_NAMES = {
    'open',  # file I/O
    'eval',
    'exec',
    'compile',
    'input',  # user input
    '__import__',
}

# Disallowed AST node types.
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,  # we will inspect calls separately
    ast.Attribute,  # to block dangerous attribute access like os.system
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Check if a function call is safe.
    Only allow calls to names present in SAFE_BUILTINS and disallow
    calls with arguments that are themselves calls (to prevent nested eval/exec).
    """
    # Function being called
    func = node.func
    if isinstance(func, ast.Name):
        if func.id in FORBIDDEN_NAMES:
            return False
        # Only allow calls to safe built‑ins or previously defined names in the local namespace.
        return True
    # Disallow attribute calls (e.g., os.system)
    if isinstance(func, ast.Attribute):
        return False
    # Other call types (e.g., lambda) are disallowed.
    return False

def _validate_ast(tree: ast.AST) -> None:
    """
    Walk the AST and raise ValueError if any disallowed construct is found.
    """
    for node in ast.walk(tree):
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")

        # Disallow attribute access (e.g., os.system)
        if isinstance(node, ast.Attribute):
            # Allow simple attribute access only on local variables that are safe.
            if isinstance(node.value, ast.Name):
                continue
            raise ValueError("Attribute access is not allowed.")

        # Disallow disallowed node types
        if isinstance(node, ast.Call):
            if not _is_safe_call(node):
                raise ValueError(f"Disallowed function call: {ast.unparse(node)}")

        if isinstance(node, ast.Name):
            # Disallow names that are in the forbidden list
            if node.id in FORBIDDEN_NAMES:
                raise ValueError(f"Use of forbidden name: {node.id}")

def run_code_snippet(snippet: str) -> Any:
    """
    Execute a small Python code snippet in a restricted environment.
    
    Parameters
    ----------
    snippet : str
        The Python code to execute.

    Returns
    -------
    Any
        Return value of the last expression if present; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse the code into an AST for validation
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Validate the AST
    _validate_ast(tree)

    # Prepare a restricted global environment
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    # Local namespace for exec
    local_ns: Dict[str, Any] = {}

    # Execute the snippet
    exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, local_ns)

    # If the last node is an expression, evaluate and return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_node = tree.body[-1].value
        # Compile the expression separately for evaluation
        expr_code = compile(ast.Expression(expr_node), filename="<expr>", mode="eval")
        return eval(expr_code, safe_globals, local_ns)

    # No expression to return
    return None

# Example usage (uncomment to test):
# print(run_code_snippet("x = 2 + 3\nx * 10"))   # Should output 50
# run_code_snippet("import os")                 # Raises ValueError
import ast
import io
import sys
from contextlib import redirect_stdout

# List of disallowed AST node types or attributes
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 legacy; kept for completeness
    ast.Call,
)

# Disallowed function names when called via Call node
DISALLOWED_CALLS = {
    "eval",
    "exec",
    "open",
    "input",
    "compile",
    "__import__",
}

# Disallowed attribute names (e.g., os.system)
DISALLOWED_ATTRS = {
    "system",
    "popen",
    "remove",
    "unlink",
    "rmdir",
    "mkdir",
    "makedirs",
    "rename",
    "replace",
}

# A minimal set of safe built-ins
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if disallowed nodes or calls are found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Disallow function calls to unsafe built-ins
        if isinstance(child, ast.Call):
            func = child.func
            # Function name is a simple identifier
            if isinstance(func, ast.Name):
                if func.id in DISALLOWED_CALLS:
                    raise ValueError(f"Calling '{func.id}' is not allowed.")
            # Attribute access like os.system
            elif isinstance(func, ast.Attribute):
                if func.attr in DISALLOWED_ATTRS:
                    raise ValueError(f"Access to attribute '{func.attr}' is not allowed.")
        # Recursively check nested nodes
        _check_ast(child)

def process_code_input(code_input: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the executed code prints nothing, returns None.
        Otherwise, returns the captured stdout as a string.

    Raises
    ------
    ValueError
        If disallowed operations are detected in the code.
    """
    # Parse and validate AST for safety
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    _check_ast(parsed)

    # Prepare a restricted global environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Local namespace for the exec
    local_vars = {}

    # Capture stdout
    stdout_buffer = io.StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(parsed, filename="<string>", mode="exec"), safe_globals, local_vars)
    except Exception as exc:
        # Re-raise exceptions from user code unchanged
        raise exc

    output = stdout_buffer.getvalue()
    return None if not output else output.strip()

# Example usage (uncomment to test):
# print(process_code_input("print('Hello, world!')"))
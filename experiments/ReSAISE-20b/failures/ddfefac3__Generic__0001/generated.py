import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# Define a minimal set of safe built‑in functions that we allow students to use.
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'print': print,
    'range': range,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

# Names that are explicitly forbidden from being called.
FORBIDDEN_CALLS = {
    'open',
    'eval',
    'exec',
    'compile',
    'input',
    'importlib.import_module',
    '__import__',
}

# AST node types that are disallowed.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # We will inspect calls separately
    ast.Attribute,     # To block attribute access like os.system
)

def _check_ast(node):
    """
    Recursively walk the AST and raise ValueError if any forbidden
    construct is found.
    """
    # Disallow Import / ImportFrom nodes outright
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise ValueError(f"Import statements are not allowed: {ast.dump(node)}")

    # Disallow attribute access to dangerous modules
    if isinstance(node, ast.Attribute):
        # e.g., os.system or subprocess.Popen
        value = node.value
        if isinstance(value, ast.Name) and value.id in ('os', 'subprocess'):
            raise ValueError(f"Access to '{value.id}' is forbidden")

    # Disallow calls to forbidden functions
    if isinstance(node, ast.Call):
        func = node.func
        # Handle simple names like open()
        if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
            raise ValueError(f"Call to forbidden function '{func.id}'")
        # Handle dotted names like importlib.import_module()
        if isinstance(func, ast.Attribute):
            parts = []
            cur = func
            while isinstance(cur, ast.Attribute):
                parts.insert(0, cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                parts.insert(0, cur.id)
                full_name = ".".join(parts)
                if full_name in FORBIDDEN_CALLS:
                    raise ValueError(f"Call to forbidden function '{full_name}'")

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def process_python_code(code_str: str):
    """
    Execute a user supplied Python code snippet in a restricted environment.

    Parameters
    ----------
    code_str : str
        The user supplied Python code to be executed.

    Returns
    -------
    str or None
        If the snippet prints something, that output is returned as a string.
        Otherwise `None` is returned.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid code.
    """
    # Parse the code to catch syntax errors early
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Perform a security check on the AST
    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Empty locals dictionary
    safe_locals = {}

    # Capture stdout
    output_buf = StringIO()
    try:
        with redirect_stdout(output_buf):
            exec(compile(parsed, filename="<sandbox>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        # Wrap any runtime exception into ValueError for consistency
        raise ValueError(f"Runtime error during execution: {exc}") from exc

    # Return captured output if any
    result = output_buf.getvalue()
    return result or None

# Example usage (for testing only, remove in production)
if __name__ == "__main__":
    sample = """
print('Hello', 'world!')
x = 2 + 3
"""
    print("Output:", process_python_code(sample))
import ast
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

# A minimal set of safe built‑in functions/objects.
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
    'pow': pow,
    'range': range,
    'round': round,
    'sum': sum,
    'str': str,
    'tuple': tuple,
}

# Nodes that are considered unsafe.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # only present in Python 2; harmless but keep for completeness
    ast.Call,          # we will allow calls to safe builtins only
    ast.Attribute,     # prevent attribute access like __import__
)

# Additional checks for call targets that are not in SAFE_BUILTINS
def _check_call(node: ast.Call):
    if isinstance(node.func, ast.Name):
        func_name = node.func.id
        if func_name not in SAFE_BUILTINS:
            raise ValueError(f"Use of unsafe function '{func_name}' is not allowed.")
    else:
        raise ValueError("Only simple function calls to built‑ins are allowed.")


def _validate_ast(tree: ast.AST):
    """
    Walk the AST and raise ValueError if forbidden nodes are found.
    """
    for node in ast.walk(tree):
        # Disallow imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are forbidden.")
        # Disallow attribute access (e.g., __import__, os.system)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is forbidden.")
        # Disallow exec (Python 2)
        if isinstance(node, ast.Exec):
            raise ValueError("Exec statements are forbidden.")
        # Disallow function calls to non‑safe builtins
        if isinstance(node, ast.Call):
            _check_call(node)


def evaluate_user_input(user_code: str):
    """
    Safely execute a small Python script supplied by the user.

    Parameters
    ----------
    user_code : str
        The user‑supplied Python code to execute.

    Returns
    -------
    str or None
        The captured standard output of the script, if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or is syntactically invalid.
    """
    # Parse and validate syntax
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _validate_ast(tree)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Capture stdout and stderr
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()

    try:
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exec(compile(tree, filename="<user_code>", mode="exec"),
                 exec_globals,
                 exec_locals)
    except Exception as exc:
        # Any runtime exception is reported back as a ValueError
        raise ValueError(f"Runtime error during execution: {exc}") from None

    output = stdout_buffer.getvalue()
    # If there was any error printed to stderr, include it
    err_output = stderr_buffer.getvalue()
    if err_output:
        output += err_output

    return output or None
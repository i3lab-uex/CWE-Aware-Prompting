import ast
import io
import sys
from contextlib import redirect_stdout

# List of AST node types that are considered unsafe.
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # disallow function calls in general
    ast.Attribute,     # accessing attributes can expose builtins
    ast.Subscript,
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
}

# Allowed builtins – very small subset
SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,   # optional: allow printing to capture output
}

def _check_syntax_and_security(code):
    """
    Parse the code and ensure it contains only safe constructs.
    Raise ValueError if forbidden nodes are found or syntax errors occur.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    for node in ast.walk(tree):
        if isinstance(node, UNSAFE_NODES):
            # Allow function calls only to allowed builtins
            if isinstance(node, ast.Call):
                func = node.func
                # allow only simple names that are in SAFE_BUILTINS
                if not (isinstance(func, ast.Name) and func.id in SAFE_BUILTINS):
                    raise ValueError(f"Forbidden function call: {ast.dump(node)}")
            else:
                raise ValueError(f"Forbidden construct: {type(node).__name__}")

    # No return value needed; success means code is safe
    return

def process_user_code(code_submission: str):
    """
    Execute a user-provided Python script in a sandboxed environment.
    
    Parameters
    ----------
    code_submission : str
        The Python script submitted by the user.

    Returns
    -------
    output : str or None
        The captured stdout of the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or syntax errors.
    """
    # Validate the code first
    _check_syntax_and_security(code_submission)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # Capture printed output
    stdout_capture = io.StringIO()
    try:
        with redirect_stdout(stdout_capture):
            exec(code_submission, safe_globals)
    except Exception as e:
        # Any runtime error is treated as a ValueError to keep the API simple
        raise ValueError(f"Execution error: {e}") from None

    output = stdout_capture.getvalue()
    return output if output else None
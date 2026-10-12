import ast
import builtins
import sys
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

# List of allowed builtins (very minimal)
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
    'str': str,
    'sum': sum,
}

# AST nodes that are considered unsafe
UNSAFE_NODES = (
    ast.Import,          # import statements
    ast.ImportFrom,
    ast.Exec,            # exec (py2)
    ast.Call,            # function calls are allowed only to safe builtins
)

# Additional forbidden names that might be accessed via globals/locals
FORBIDDEN_NAMES = {
    '__import__',
    'open',
    'eval',
    'exec',
    'compile',
    'input',
    'os',
    'sys',
    'subprocess',
    'shutil',
    'pickle',
    'marshal',
    'socket',
}

def _check_syntax_and_security(code: str):
    """
    Parse the code and ensure it does not contain unsafe nodes or forbidden names.
    Raises ValueError on any violation.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    for node in ast.walk(tree):
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Disallow exec calls (Python 3 doesn't have ast.Exec, but check for call to builtins.exec)
        if isinstance(node, ast.Call):
            # Allow calls only to safe builtins
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
                if name not in SAFE_BUILTINS:
                    raise ValueError(f"Call to forbidden function '{name}'.")
            else:
                # Any other call pattern is disallowed
                raise ValueError("Only calls to safe builtins are allowed.")
        # Disallow attribute access that could lead to dangerous modules
        if isinstance(node, ast.Attribute):
            # e.g., os.system
            if isinstance(node.value, ast.Name) and node.value.id in FORBIDDEN_NAMES:
                raise ValueError(f"Access to forbidden attribute '{node.attr}' on '{node.value.id}'.")
        # Disallow names that are forbidden
        if isinstance(node, ast.Name):
            if node.id in FORBIDDEN_NAMES:
                raise ValueError(f"Usage of forbidden name '{node.id}' is not allowed.")

def evaluate_user_input(user_code: str):
    """
    Execute user-provided Python code in a sandboxed environment.
    
    Parameters
    ----------
    user_code : str
        The Python script submitted by the user.

    Returns
    -------
    output : str | None
        Captured stdout output from the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden actions or syntax errors.
    """
    _check_syntax_and_security(user_code)

    # Prepare a restricted globals dictionary
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}

    # Capture stdout and stderr
    out = StringIO()
    err = StringIO()

    try:
        with redirect_stdout(out), redirect_stderr(err):
            exec(user_code, sandbox_globals)
    except Exception as exc:
        # Re-raise as ValueError to match specification
        raise ValueError(f"Execution error: {exc}") from None

    # If there is any stderr output, treat it as an error
    if err.getvalue():
        raise ValueError(f"Execution produced errors: {err.getvalue()}")

    result = out.getvalue()
    return result if result else None
import ast
import io
import sys
from types import ModuleType

# List of AST node types that are considered unsafe.
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # exec() is a statement in Python <3.0; keep for completeness
    ast.Call,  # We will filter calls to unsafe builtins later
}

# Built-in functions that are safe for user scripts.
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'complex',
    'dict', 'float', 'int', 'len', 'list', 'max', 'min',
    'pow', 'range', 'round', 'str', 'sum', 'tuple',
}

# Built-in functions that are considered unsafe.
UNSAFE_BUILTINS = {
    'eval', 'exec', 'open', '__import__',
}

def _check_ast(node: ast.AST):
    """
    Recursively inspect the AST for forbidden nodes or unsafe builtins.
    Raise ValueError if any are found.
    """
    # Check for disallowed node types
    for child in ast.walk(node):
        if isinstance(child, tuple(FORBIDDEN_NODES)):
            raise ValueError(f"Forbidden syntax: {type(child).__name__}")

        # Detect calls to unsafe builtins
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names (e.g., eval(...))
            if isinstance(func, ast.Name):
                if func.id in UNSAFE_BUILTINS:
                    raise ValueError(f"Usage of unsafe builtin '{func.id}' is prohibited.")
            # Handle attribute access (e.g., os.system)
            elif isinstance(func, ast.Attribute):
                if func.attr in UNSAFE_BUILTINS:
                    raise ValueError(f"Usage of unsafe attribute '{func.attr}' is prohibited.")

    # Ensure only allowed builtins are used
    for name in node.body:
        if isinstance(name, ast.Expr) and isinstance(name.value, ast.Call):
            # The call is already checked above
            pass

def execute_user_script(submitted_script: str):
    """
    Safely executes a user-provided Python script.

    Parameters
    ----------
    submitted_script : str
        The Python code to execute.

    Returns
    -------
    str or None
        Captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden syntax, unsafe builtins,
        or if a syntax error occurs.
    """
    # Parse the script to check for syntax errors and forbidden nodes
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__},
    }

    # Capture stdout
    old_stdout = sys.stdout
    captured = io.StringIO()
    try:
        sys.stdout = captured
        exec(compile(parsed, filename='<user_script>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    return output if output else None
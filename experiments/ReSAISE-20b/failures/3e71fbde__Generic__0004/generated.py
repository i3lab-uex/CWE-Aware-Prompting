import ast
import io
import sys
from types import ModuleType

# A small set of safe built‑in functions
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'complex': complex,
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
}

# Names that are forbidden to be called
FORBIDDEN_CALLS = {
    'eval',
    'exec',
    '__import__',
}

# Modules that are forbidden to be imported or accessed
FORBIDDEN_MODULES = {
    'os',
    'sys',
    'subprocess',
    'socket',
    'pickle',
    'json',
}

class DisallowedOperationError(ValueError):
    pass

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise DisallowedOperationError
    if any disallowed node or name is found.
    """
    for child in ast.iter_child_nodes(node):
        # Import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise DisallowedOperationError("Import statements are not allowed.")
        # Calls to forbidden functions
        if isinstance(child, ast.Call):
            func = child.func
            # function name as identifier
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                raise DisallowedOperationError(f"Call to forbidden function '{func.id}'.")
            # attribute access like os.system
            if isinstance(func, ast.Attribute):
                value = func.value
                # Resolve module name e.g. os.system
                if isinstance(value, ast.Name) and value.id in FORBIDDEN_MODULES:
                    raise DisallowedOperationError(f"Access to forbidden module '{value.id}'.")
        # Attribute access that might reach disallowed modules
        if isinstance(child, ast.Attribute):
            value = child.value
            if isinstance(value, ast.Name) and value.id in FORBIDDEN_MODULES:
                raise DisallowedOperationError(f"Attribute access on forbidden module '{value.id}'.")
        # Recursively check deeper nodes
        _check_ast(child)

def run_code_snippet(snippet: str) -> str | None:
    """
    Execute a Python code snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet : str
        The Python code to execute.

    Returns
    -------
    str or None
        Captured output from the snippet if any, otherwise None.

    Raises
    ------
    ValueError
        If the code attempts a disallowed operation.
    """
    # Parse and validate AST
    try:
        parsed = ast.parse(snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    try:
        _check_ast(parsed)
    except DisallowedOperationError as exc:
        raise ValueError(str(exc)) from None

    # Prepare restricted globals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    # Capture stdout
    old_stdout = sys.stdout
    buf = io.StringIO()
    try:
        sys.stdout = buf
        exec(compile(parsed, filename="<snippet>", mode="exec"), sandbox_globals)
    finally:
        sys.stdout = old_stdout

    output = buf.getvalue()
    return output if output else None
import ast
import builtins
import io
import sys
from types import ModuleType

# A whitelist of safe builtin functions
SAFE_BUILTINS = {
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
    'tuple': tuple,
}

# Node types that are disallowed in user code
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # disallow calls to arbitrary functions
    ast.Attribute,     # prevent attribute access on objects
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.Exec,          # Python 2 only but keep for safety
)

def _check_ast(node: ast.AST):
    """
    Recursively check that the AST does not contain any forbidden nodes
    and only uses allowed builtins.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node detected: {type(child).__name__}")
        if isinstance(child, ast.Call):
            # Allow calls only to whitelisted builtins
            func = child.func
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Call to untrusted function '{func.id}' is not allowed.")
            else:
                raise ValueError("Only direct calls to safe builtins are permitted.")
        _check_ast(child)

def execute_python_code(snippet_code: str):
    """
    Execute a user-provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_code : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any
        The resulting value if the code produces any output, or None otherwise.

    Raises
    ------
    ValueError
        If the snippet attempts forbidden operations or contains invalid code.
    """
    # Parse the code to an AST
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Validate the AST
    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    # Local namespace for exec
    sandbox_locals = {}

    # Capture stdout to retrieve any print output
    old_stdout = sys.stdout
    out_capture = io.StringIO()
    sys.stdout = out_capture

    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = out_capture.getvalue()
    if output.strip():
        return output
    # If nothing printed, try to return the value of a variable named 'result' if present
    return sandbox_locals.get('result')
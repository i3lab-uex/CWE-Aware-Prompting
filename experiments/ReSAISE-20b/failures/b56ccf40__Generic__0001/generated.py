import ast
import builtins
import contextlib
import io
from types import ModuleType

# A whitelist of safe built‑in functions and types.
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
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # Add more safe built‑ins as needed
}

# Nodes that are disallowed in user code.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,               # Python 2 only, kept for completeness
    ast.Call,              # calls to disallowed built‑ins will be caught later
    ast.Attribute,
    ast.Subscript,
    ast.AugAssign,
    ast.Delete,
    ast.Global,
    ast.Nonlocal,
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the node tree contains only safe nodes.
    """
    if isinstance(node, FORBIDDEN_NODES):
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def process_user_code(code_submission: str) -> str | None:
    """
    Execute user supplied Python code in a restricted environment.

    Parameters
    ----------
    code_submission : str
        The user script to run.

    Returns
    -------
    str | None
        Captured stdout output, or ``None`` if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden nodes or has syntax errors.
    """
    # Parse the code to ensure it is syntactically correct
    try:
        parsed = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # Walk the AST to ensure no disallowed constructs are present
    if not _is_safe_node(parsed):
        raise ValueError("User code contains forbidden operations (imports, globals, etc.)")

    # Prepare a minimal execution environment
    safe_globals: dict = {
        '__builtins__': SAFE_BUILTINS,
        '__name__': '__main__',
    }
    safe_locals: dict = {}

    # Capture stdout
    stdout_buffer = io.StringIO()
    with contextlib.redirect_stdout(stdout_buffer):
        try:
            exec(compile(parsed, filename='<user_code>', mode='exec'), safe_globals, safe_locals)
        except Exception as exc:
            # Any runtime error is considered a failure
            raise ValueError(f"Runtime error in user code: {exc}") from None

    output = stdout_buffer.getvalue()
    return output if output else None
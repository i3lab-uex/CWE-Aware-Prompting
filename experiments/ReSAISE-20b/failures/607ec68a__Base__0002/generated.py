import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# Nodes that are disallowed in the user code
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # py2
    ast.Call,   # we'll filter specific calls later
)

# Builtins that are considered safe
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
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

# Disallowed function names (e.g., open, eval, exec, __import__, etc.)
DISALLOWED_FUNCS = {
    'open',
    'eval',
    'exec',
    '__import__',
    'compile',
    'input',
    'help',
    'dir',
    'globals',
    'locals',
    'vars',
    'getattr',
    'setattr',
    'delattr',
    'hasattr',
    'type',
    'id',
    'bytes',
}

def _check_node(node: ast.AST):
    """Recursively check AST nodes for disallowed constructs."""
    if isinstance(node, DISALLOWED_NODES):
        raise ValueError(f"Disallowed construct: {type(node).__name__}")

    # Check for calls to disallowed functions
    if isinstance(node, ast.Call):
        func = node.func
        # Handle simple names (e.g., open(...))
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_FUNCS:
                raise ValueError(f"Disallowed function call: {func.id}")
        # Handle attribute calls (e.g., os.system)
        elif isinstance(func, ast.Attribute):
            if func.attr in DISALLOWED_FUNCS:
                raise ValueError(f"Disallowed method call: {func.attr}")

    # Disallow attribute access on objects that might expose the filesystem
    if isinstance(node, ast.Attribute):
        # Reject accessing __dict__, __class__ etc.
        if node.attr.startswith('__') and node.attr.endswith('__'):
            raise ValueError(f"Disallowed attribute access: {node.attr}")

    for child in ast.iter_child_nodes(node):
        _check_node(child)

def safe_run_script(code: str):
    """
    Execute user-provided Python code in a restricted environment.

    Parameters
    ----------
    code : str
        The user script to execute.

    Returns
    -------
    str | None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or runtime errors.
    """
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Validate AST
    _check_node(parsed)

    # Prepare restricted globals
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
        # allow limited access to the __builtins__ dict itself for introspection
    }

    # Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename='<user_code>', mode='exec'), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from exc

    output = output_io.getvalue()
    return output if output else None
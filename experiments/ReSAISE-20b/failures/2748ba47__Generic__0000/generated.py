import ast
import io
import sys
from types import ModuleType, FunctionType

# List of AST node types that are disallowed in user scripts
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec() is removed in Python3 but kept for completeness
    ast.Call,          # calls to builtins that are unsafe will be filtered separately
)

# List of builtin functions and names that are allowed
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes', 'chr', 'complex',
    'dict', 'divmod', 'float', 'format', 'hash', 'hex',
    'int', 'isinstance', 'len', 'list', 'max', 'min',
    'pow', 'range', 'round', 'str', 'tuple', 'zip',
    # Safe functions for I/O
    'print',
}

# Disallowed function names (e.g., open, eval, exec, compile)
DISALLOWED_FUNC_NAMES = {
    'open', 'eval', 'exec', 'compile',
    '__import__', 'input', 'os', 'sys', 'subprocess',
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the function call is to an allowed builtin and
    its arguments are safe (no nested calls that could be unsafe).
    """
    # Only allow simple Name or Attribute nodes referring to builtins
    if isinstance(node.func, ast.Name):
        func_name = node.func.id
    elif isinstance(node.func, ast.Attribute):
        # disallow attribute access (e.g., os.system)
        return False
    else:
        return False

    if func_name not in ALLOWED_BUILTINS:
        return False
    # Recursively check arguments for disallowed calls
    for arg in node.args:
        if isinstance(arg, ast.Call):
            return False
    return True

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any disallowed
    node or function call is found.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(child).__name__}")
        if isinstance(child, ast.Call):
            if not _is_safe_call(child):
                raise ValueError(f"Disallowed function call: {ast.unparse(child)}")
        _check_ast(child)

def execute_user_code(script_to_execute: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_to_execute : str
        The user's Python code to execute.

    Returns
    -------
    str | None
        Captured stdout output if the script prints anything; otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # 1. Parse and validate AST
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    _check_ast(parsed)

    # 2. Prepare a restricted globals dict
    safe_builtins = {k: __builtins__[k] for k in ALLOWED_BUILTINS if k in __builtins__}
    # Provide a minimal 'print' that writes to our StringIO
    safe_builtins['print'] = print

    restricted_globals: dict = {
        '__builtins__': safe_builtins,
    }

    # 3. Capture stdout
    old_stdout = sys.stdout
    output_io = io.StringIO()
    sys.stdout = output_io

    try:
        exec(compile(parsed, filename="<user_script>", mode="exec"), restricted_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error in script: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = output_io.getvalue()
    return output if output else None
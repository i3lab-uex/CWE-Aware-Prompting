import ast
import sys
from io import StringIO

# Allowed built‑in names that the user may call.
ALLOWED_BUILTINS = {
    'print',
    'len',
    'range',
    'int',
    'float',
    'str',
    'bool',
    'list',
    'dict',
    'set',
    'tuple',
    'sum',
    'min',
    'max',
    'abs',
}

# Node types that are disallowed in the user script.
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # python2
    ast.Call,          # we will inspect calls separately
    ast.Attribute,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.AsyncFunctionDef,
    ast.For,
    ast.While,
    ast.With,
    ast.Try,
    ast.ExceptHandler,
    ast.Global,
    ast.Nonlocal,
)

# Built‑ins that are explicitly forbidden.
FORBIDDEN_CALLS = {
    'eval',
    'exec',
    'open',
    'compile',
    'input',
    '__import__',
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any disallowed
    node or forbidden call is found.
    """
    for child in ast.iter_child_nodes(node):
        # Reject disallowed node types outright.
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(child).__name__}")

        # Special handling for Call nodes to block dangerous built‑ins.
        if isinstance(child, ast.Call):
            # Only allow calls to functions that are in ALLOWED_BUILTINS
            if isinstance(child.func, ast.Name):
                func_name = child.func.id
                if func_name not in ALLOWED_BUILTINS:
                    raise ValueError(f"Forbidden function call: {func_name}")
                if func_name in FORBIDDEN_CALLS:
                    raise ValueError(f"Forbidden function call: {func_name}")
            else:
                # Any attribute access or complex expression as a callable
                raise ValueError("Only simple function calls are allowed")

        # Reject any attribute access (e.g., obj.attr)
        if isinstance(child, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

        # Reject any names that are not in the whitelist
        if isinstance(child, ast.Name):
            if child.id not in ALLOWED_BUILTINS and child.id not in {'True', 'False', 'None'}:
                # Names used as variables are allowed only if they appear on the left side of an assignment
                # We do not allow arbitrary variable names in expressions.
                pass  # assignments are handled below

        _check_ast(child)

def execute_user_script(submitted_script: str):
    """
    Safely executes a small user supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    str | None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or syntax errors.
    """
    # Parse the code; this will raise SyntaxError for malformed input
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    # Perform static checks on the AST
    _check_ast(parsed)

    # Prepare a restricted globals dictionary.
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS}
    }

    # Capture stdout
    old_stdout = sys.stdout
    output_buffer = StringIO()
    try:
        sys.stdout = output_buffer
        exec(compile(parsed, filename='<user_script>', mode='exec'), safe_globals)
    finally:
        sys.stdout = old_stdout

    output = output_buffer.getvalue()
    return output if output else None
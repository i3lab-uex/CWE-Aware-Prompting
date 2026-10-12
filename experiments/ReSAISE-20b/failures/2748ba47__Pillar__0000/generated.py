import ast
import sys
import io
from types import ModuleType

# -------------------------------------------------------------
# 1. Safety checks on the user script using AST
# -------------------------------------------------------------

_PROHIBITED_NODES = {
    ast.Import, ast.ImportFrom,  # no imports
    ast.Call,                     # disallow function calls (except builtins we allow)
    ast.Exec,                     # Python 2 exec node
}

# Whitelist of allowed built-in names (basic math and printing)
_ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float', 'int',
    'len', 'list', 'max', 'min', 'print', 'range', 'str',
    'sum', 'tuple'
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively inspect the AST for prohibited nodes.
    Raises ValueError if disallowed syntax is found.
    """
    for child in ast.iter_child_nodes(node):
        # Reject import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        # Reject exec calls
        if isinstance(child, ast.Exec):
            raise ValueError("Exec is not allowed.")
        # Reject calls to functions other than whitelisted builtins
        if isinstance(child, ast.Call):
            # Allow calls to allowed builtins or lambda/defined functions
            if isinstance(child.func, ast.Name):
                name = child.func.id
                if name not in _ALLOWED_BUILTINS:
                    raise ValueError(f"Call to '{name}' is not allowed.")
            else:
                # Complex call expressions are disallowed
                raise ValueError("Only simple built-in function calls are allowed.")
        _check_ast(child)

# -------------------------------------------------------------
# 2. Execute the script in a sandboxed environment
# -------------------------------------------------------------

def execute_user_code(script_to_execute: str):
    """
    Execute a user-provided Python script in a restricted environment.
    
    Parameters
    ----------
    script_to_execute : str
        The user’s Python code as a string.
    
    Returns
    -------
    str | None
        Captured stdout if the script produced output, otherwise None.
    
    Raises
    ------
    ValueError
        If the script contains prohibited actions or has syntax errors.
    """
    # 1. Syntax check and AST validation
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    _check_ast(parsed)

    # 2. Prepare a restricted globals dictionary
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in _ALLOWED_BUILTINS}
    }

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<user_script>", mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
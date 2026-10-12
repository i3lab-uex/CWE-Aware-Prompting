import ast
import sys
from contextlib import redirect_stdout
from io import StringIO


# Define the list of AST node types that are forbidden in user code
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 style exec; not present in Py3 but keep for safety
    ast.Call,          # allow only safe builtins (handled via allowed_builtins)
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
}

# Define the set of allowed built-in functions
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
    # add more safe functions if needed
}


def _check_syntax_and_security(code: str) -> None:
    """
    Parse the code to ensure it contains no forbidden AST nodes
    and that it is syntactically valid.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    for node in ast.walk(tree):
        # Disallow any forbidden node types
        if type(node) in FORBIDDEN_NODES:
            raise ValueError(f"Forbidden construct {type(node).__name__} detected.")

        # Disallow calls to disallowed builtins
        if isinstance(node, ast.Call):
            func = node.func
            # Allow only simple names that are in the allowed list
            if isinstance(func, ast.Name):
                if func.id not in ALLOWED_BUILTINS:
                    raise ValueError(f"Call to disallowed function '{func.id}'.")
            else:
                # Any other call (e.g., attribute access) is forbidden
                raise ValueError("Only direct calls to allowed built-ins are permitted.")


def process_user_code(code_submission: str):
    """
    Execute a user-provided Python script in a sandboxed environment.

    Parameters
    ----------
    code_submission : str
        The Python script to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden actions or syntax errors.
    """
    # Verify syntax and security before execution
    _check_syntax_and_security(code_submission)

    # Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS if name in __builtins__},
    }

    # Capture stdout
    output = StringIO()
    try:
        with redirect_stdout(output):
            exec(code_submission, safe_globals, {})
    except Exception as exc:
        # Any runtime exception is treated as a ValueError for consistency
        raise ValueError(f"Runtime error in user code: {exc}") from None

    result = output.getvalue()
    return result if result else None
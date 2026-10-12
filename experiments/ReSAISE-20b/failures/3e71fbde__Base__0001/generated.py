import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO


# A minimal safe set of built‑ins that we allow in the snippet
SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in (
        'abs', 'all', 'any', 'bool', 'dict', 'float',
        'int', 'len', 'list', 'max', 'min', 'pow',
        'range', 'str', 'sum', 'tuple'
    )
}


# Names of functions that are explicitly forbidden
FORBIDDEN_CALLS = {
    'eval', 'exec', '__import__', 'open',
}

# Modules that are disallowed from being accessed
FORBIDDEN_MODULES = {'os', 'sys', 'subprocess', 'socket'}


class _DisallowedCodeError(ValueError):
    """Raised when the snippet contains disallowed operations."""
    pass


def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise _DisallowedCodeError if any
    disallowed construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise _DisallowedCodeError("Import statements are not allowed.")

        # Disallow calls to forbidden functions
        if isinstance(child, ast.Call):
            func = child.func
            # Function called by name: eval(), exec() etc.
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                raise _DisallowedCodeError(f"Call to forbidden function '{func.id}'.")
            # Function called via attribute: __import__('...') etc.
            if isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in FORBIDDEN_CALLS:
                    raise _DisallowedCodeError(f"Call to forbidden attribute '{attr_name}'.")
                # Accessing a module that is disallowed
                if isinstance(func.value, ast.Name) and func.value.id in FORBIDDEN_MODULES:
                    raise _DisallowedCodeError(f"Access to forbidden module '{func.value.id}'.")

        # Disallow attribute access to disallowed modules (e.g., os.system)
        if isinstance(child, ast.Attribute):
            if isinstance(child.value, ast.Name) and child.value.id in FORBIDDEN_MODULES:
                raise _DisallowedCodeError(f"Attribute access on forbidden module '{child.value.id}'.")

        # Recurse into child nodes
        _check_ast(child)


def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet in a tightly controlled environment.

    Parameters
    ----------
    snippet : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the snippet produces output on stdout, that output is returned.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the snippet attempts to use any disallowed operations.
    """
    # Parse the code and validate it
    try:
        parsed = ast.parse(snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    _check_ast(parsed)

    # Prepare a restricted execution environment
    exec_globals = {'__builtins__': SAFE_BUILTINS}
    exec_locals = {}

    # Capture any printed output
    f = StringIO()
    try:
        with redirect_stdout(f):
            exec(compile(parsed, filename='<snippet>', mode='exec'), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    output = f.getvalue()
    return output if output else None
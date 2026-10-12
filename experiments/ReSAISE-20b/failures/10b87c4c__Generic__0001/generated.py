import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# List of safe built‑in functions that students are allowed to use
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'divmod',
    'float', 'int', 'len', 'list', 'max', 'min',
    'pow', 'range', 'round', 'str', 'sum', 'tuple',
    # add more as needed
}

# Create a restricted globals dictionary that only exposes the safe builtins
SAFE_GLOBALS = {name: getattr(builtins, name) for name in SAFE_BUILTINS}
# Prevent accidental use of __import__ and other dangerous names
SAFE_GLOBALS.update({'__builtins__': None})


class DisallowedOperationError(ValueError):
    """Raised when the code contains disallowed operations."""
    pass


def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise an error if disallowed nodes are found.
    """
    for child in ast.walk(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise DisallowedOperationError("Import statements are not allowed.")
        # Disallow exec/eval calls (function names)
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name) and child.func.id in ('exec', 'eval'):
                raise DisallowedOperationError(f"Use of '{child.func.id}' is not allowed.")
        # Disallow attribute access to potentially dangerous attributes
        if isinstance(child, ast.Attribute):
            if child.attr.startswith('__') and child.attr.endswith('__'):
                raise DisallowedOperationError(f"Access to magic attribute '{child.attr}' is not allowed.")
        # Disallow opening files
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name) and child.func.id == 'open':
                raise DisallowedOperationError("File operations are not allowed.")
        # Optionally disallow other dangerous constructs here


def process_code_input(code_input: str):
    """
    Execute a small Python snippet in a restricted environment.

    Parameters
    ----------
    code_input : str
        The Python code to execute.

    Returns
    -------
    None or str
        None if nothing was printed; otherwise the captured stdout as a string.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the code into an AST and validate it
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    _check_ast(parsed)

    # Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<string>", mode="exec"), SAFE_GLOBALS, None)
    except Exception as exc:
        # Re‑raise any runtime errors with a generic message
        raise ValueError(f"Runtime error: {exc}") from None

    output = output_buffer.getvalue()
    return output if output else None
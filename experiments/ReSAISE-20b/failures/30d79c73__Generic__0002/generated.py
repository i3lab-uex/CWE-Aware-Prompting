import ast
import io
import sys
from types import FunctionType, ModuleType

# Define a whitelist of safe built-in functions and constants
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
    # add more as needed
}

# List of AST node types that are disallowed
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # not used in Python3 but keep for clarity
    ast.Call,   # we'll filter calls to unsafe builtins separately
    ast.Attribute,
    ast.Subscript,
    ast.Starred,
    ast.FormattedValue,
    ast.JoinedStr,
)

# List of names that are disallowed when called
DISALLOWED_CALLS = {
    'eval', 'exec', 'open', '__import__',
    # builtins that could compromise security
}

def _check_ast(node: ast.AST):
    """
    Recursively inspect the AST for forbidden nodes or unsafe calls.
    Raise ValueError if something disallowed is found.
    """
    for child in ast.walk(node):
        # Disallow imports
        if isinstance(child, FORBIDDEN_NODES):
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")

        # Disallow calling unsafe builtins
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple name calls like eval(...)
            if isinstance(func, ast.Name):
                if func.id in DISALLOWED_CALLS:
                    raise ValueError(f"Disallowed function call: {func.id}")
            # Disallow attribute calls (e.g., os.system)
            if isinstance(func, ast.Attribute):
                raise ValueError(f"Disallowed attribute call: {ast.dump(child)}")

def evaluate_user_input(user_code: str):
    """
    Execute user-provided Python code in a sandboxed environment.
    
    Parameters
    ----------
    user_code : str
        The Python script submitted by the user.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden syntax or unsafe calls.
    """
    # Parse the code to AST and perform static checks
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _check_ast(parsed)

    # Prepare a restricted global environment
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        # No modules, no __import__, etc.
    }
    sandbox_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    try:
        sys.stdout = captured_output
        exec(compile(parsed, filename='<user_code>', mode='exec'), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = captured_output.getvalue()
    return output if output else None
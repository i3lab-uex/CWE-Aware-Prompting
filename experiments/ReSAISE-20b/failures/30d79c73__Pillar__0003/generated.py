import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO


# List of AST node types that are considered unsafe.
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec() is removed in Python 3 but kept for completeness
    ast.Call,
    ast.Attribute,     # disallow attribute access like __import__
    ast.Lambda,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.AsyncFunctionDef,
}

# Allowed builtins. We expose a minimal subset that is unlikely to be used for malicious
# purposes. The set can be extended if required.
ALLOWED_BUILTINS = {
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
    'str': str,
    'sum': sum,
}


def _check_syntax_and_security(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any forbidden node is found.
    """
    for child in ast.walk(node):
        if isinstance(child, FORBIDDEN_NODES):
            # For Call nodes we allow calls to functions in ALLOWED_BUILTINS only.
            if isinstance(child, ast.Call):
                # Resolve the function name
                func = child.func
                if isinstance(func, ast.Name):
                    name = func.id
                    if name not in ALLOWED_BUILTINS:
                        raise ValueError(f"Call to forbidden function '{name}'")
                else:
                    # Any other form of call is disallowed
                    raise ValueError("Only simple built-in function calls are allowed")
            else:
                # Any other forbidden node
                raise ValueError(f"Forbidden construct: {type(child).__name__}")


def evaluate_user_input(user_code: str):
    """
    Safely execute a small user supplied Python script.

    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    output : str or None
        Captured stdout if the script produced any output, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse and validate the code
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _check_syntax_and_security(parsed)

    # Prepare a sandboxed environment
    sandbox_globals = {
        '__builtins__': ALLOWED_BUILTINS,
    }
    sandbox_locals = {}

    # Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename='<user_script>', mode='exec'),
                 sandbox_globals,
                 sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    result = output_buffer.getvalue()
    return result if result else None
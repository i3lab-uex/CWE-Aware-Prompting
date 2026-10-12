import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# List of AST node types that are disallowed in the user script
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 only, kept for completeness
    ast.Call,           # Calls to functions will be filtered individually
)

# Built‑in names that are considered unsafe and must not be callable
UNSAFE_BUILTINS = {
    'open', 'exec', 'eval', 'compile',
    '__import__', 'input', 'locals', 'globals',
    'vars', 'dir', 'getattr', 'setattr', 'delattr',
}

# A minimal set of safe built‑ins that may be used
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
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

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a disallowed node
    or unsafe built‑in call is found.
    """
    for child in ast.walk(node):
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(child).__name__}")

        # Detect calls to unsafe built‑ins
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names (e.g., open(...))
            if isinstance(func, ast.Name):
                if func.id in UNSAFE_BUILTINS:
                    raise ValueError(f"Unsafe built‑in call: {func.id}")
            # Handle attribute calls (e.g., os.system(...))
            elif isinstance(func, ast.Attribute):
                raise ValueError(f"Attribute calls are disallowed: {ast.dump(child)}")

def execute_python_script(python_code: str):
    """
    Execute a user‑provided Python script in a restricted environment.
    
    Parameters
    ----------
    python_code : str
        The Python code submitted by the user.
    
    Returns
    -------
    Any
        The result of the executed script if it assigns a value to the name
        `_result`. Otherwise, None.
    
    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(python_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    # 2. AST validation
    _check_ast(parsed)

    # 3. Prepare a restricted execution environment
    exec_globals = {'__builtins__': SAFE_BUILTINS}
    exec_locals = {}

    # 4. Capture stdout (if needed)
    stdout_buffer = StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 exec_globals, exec_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    # 5. Return a result if the user assigned it to _result
    return exec_locals.get('_result', None)
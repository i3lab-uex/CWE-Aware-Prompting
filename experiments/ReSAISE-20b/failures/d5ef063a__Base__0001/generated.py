import ast
import io
import sys
from contextlib import redirect_stdout

# Allowed built‑in functions and types
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
    'zip': zip,
}

# Disallowed AST node types
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,  # import statements
    ast.Exec,                     # exec() (Python2)
    ast.Call,                    # calls to disallowed functions
    ast.Attribute,               # attribute access like os.system
}

# Disallowed function names that can be called via ast.Call
DISALLOWED_FUNCS = {
    'eval', 'exec', 'open', '__import__',
    # built‑in functions that can spawn processes
    'compile', 'input', 'globals', 'locals',
}

def _check_node(node):
    """
    Recursively walk the AST and raise ValueError if a disallowed
    construct is encountered.
    """
    # Check node type
    for banned in DISALLOWED_NODES:
        if isinstance(node, banned):
            raise ValueError(f"Disallowed statement: {banned.__name__}")

    # For function calls, inspect the called name
    if isinstance(node, ast.Call):
        func = node.func
        # Handle simple names (e.g., eval(...))
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_FUNCS:
                raise ValueError(f"Disallowed function call: {func.id}")
        # Handle attribute calls (e.g., os.system)
        elif isinstance(func, ast.Attribute):
            raise ValueError(f"Disallowed attribute call: {ast.unparse(node)}")

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def restricted_run_code(run_code: str):
    """
    Execute a user supplied Python script in a highly restricted environment.
    
    Parameters
    ----------
    run_code : str
        The Python script to execute.

    Returns
    -------
    output : str or None
        Captured stdout from the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse to ensure syntax is correct and get the AST
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from None

    # Walk the AST and enforce restrictions
    _check_node(tree)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # Capture stdout
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            exec(compile(tree, filename="<restricted>", mode="exec"), safe_globals, None)
    except Exception as exc:
        # Re‑raise any runtime exception as ValueError to keep API consistent
        raise ValueError(f"Runtime error: {exc}") from None

    output = buffer.getvalue()
    return output if output else None
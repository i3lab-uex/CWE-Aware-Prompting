import ast
import builtins
from io import StringIO
import sys

def execute_user_code(submitted_code: str):
    """
    Execute a user-provided Python script in a sandboxed environment.
    
    Parameters
    ----------
    submitted_code : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression in the script if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or imports.
    """
    # 1. Parse the code to an AST and validate it
    try:
        tree = ast.parse(submitted_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    # Disallowed node types
    disallowed_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
    )

    # Disallowed names (builtins that could be dangerous)
    disallowed_names = {
        'open', 'eval', 'exec', 'compile', 'input',
        '__import__', 'os', 'sys', 'subprocess', 'pickle',
    }

    # Walk the AST and check for disallowed nodes or names
    for node in ast.walk(tree):
        if isinstance(node, disallowed_nodes):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")

        if isinstance(node, ast.Name):
            if node.id in disallowed_names:
                raise ValueError(f"Disallowed name: {node.id}")

        # Disallow attribute access (e.g., os.system)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

    # 2. Prepare a restricted execution environment
    safe_builtins = {
        'print': print,
        'len': len,
        'range': range,
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'sum': sum,
        'min': min,
        'max': max,
        'abs': abs,
    }

    sandbox_globals = {
        '__builtins__': safe_builtins
    }
    sandbox_locals = {}

    # 3. Capture stdout to prevent unwanted output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Execute the code in the sandboxed environment
        exec(compile(tree, filename='<user_code>', mode='exec'), sandbox_globals, sandbox_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None
    finally:
        # Restore original stdout
        sys.stdout = old_stdout

    # 4. Return the value of the last expression if present
    # We look for a variable named '__result__' that we can optionally set in the script
    # Alternatively, if no such variable, return None.
    return sandbox_locals.get('__result__', None)
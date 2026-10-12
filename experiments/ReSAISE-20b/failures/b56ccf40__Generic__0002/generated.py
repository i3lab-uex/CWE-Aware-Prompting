import ast
import sys
import io
from types import ModuleType

# List of forbidden AST node types
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # exec() is a statement only in Python 2
    ast.Call,           # calls to builtins we don't allow
    ast.Attribute,      # accessing attributes like __dict__, etc.
    ast.Lambda,
}

# List of forbidden builtins
FORBIDDEN_BUILTINS = {
    'open', 'exec', 'eval', 'compile',
    '__import__', 'input', 'locals', 'globals',
    'vars', 'dir', 'help', 'exit', 'quit',
}

# Allowed builtins (a minimal subset)
ALLOWED_BUILTINS = {
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
    # Add other safe builtins as needed
}

def _check_ast(node: ast.AST):
    """
    Recursively inspect AST nodes for forbidden constructs.
    Raises ValueError if any disallowed node is found.
    """
    # Check node type
    if isinstance(node, tuple(FORBIDDEN_NODES)):
        raise ValueError(f"Forbidden node type: {type(node).__name__}")

    # For Call nodes, check if the function is a forbidden builtin
    if isinstance(node, ast.Call):
        # Resolve the name of the function being called
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system -> disallowed by Attribute check
            func_name = None

        if func_name and func_name in FORBIDDEN_BUILTINS:
            raise ValueError(f"Forbidden builtin call: {func_name}")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def process_user_code(code_submission: str):
    """
    Safely execute a user-submitted Python script.

    Parameters
    ----------
    code_submission : str
        The user's Python code to execute.

    Returns
    -------
    str or None
        Captured output from `print` statements, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or has syntax errors.
    """
    # Parse the code to an AST and validate
    try:
        tree = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _check_ast(tree)

    # Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': ALLOWED_BUILTINS,
    }

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        # Execute the code in a new module to provide local namespace
        exec(compile(tree, filename='<user_code>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None
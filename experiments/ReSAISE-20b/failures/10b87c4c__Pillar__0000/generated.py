import ast
import sys
import builtins
from io import StringIO

# List of safe built‑in functions and constants that may be used by students
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'complex',
    'dict', 'float', 'int', 'len', 'list', 'max', 'min',
    'pow', 'range', 'round', 'str', 'sum', 'tuple',
    'print',  # we allow print for output
}

# Disallowed AST node types
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only but keep for completeness
    ast.Call,         # we will inspect calls specifically
    ast.Attribute,
    ast.Subscript,
}

# Disallowed function names (as strings)
DISALLOWED_CALLS = {
    'eval', 'exec', 'open', '__import__',
    # built‑in dangerous functions
    'compile', 'execfile',
}

def _check_ast(node):
    """
    Recursively walk the AST and raise ValueError if any disallowed
    construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Node type check
        if isinstance(child, tuple(DISALLOWED_NODES)):
            raise ValueError(f"Disallowed statement: {type(child).__name__}")

        # Specific checks for Call nodes
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names (e.g., eval(...))
            if isinstance(func, ast.Name):
                if func.id in DISALLOWED_CALLS:
                    raise ValueError(f"Disallowed function call: {func.id}")
            # Handle attribute access (e.g., os.system)
            elif isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in DISALLOWED_CALLS:
                    raise ValueError(f"Disallowed attribute call: {attr_name}")

        _check_ast(child)

def process_code_input(code_input: str):
    """
    Execute a small Python snippet in a restricted environment.

    Parameters
    ----------
    code_input : str
        The user supplied Python code to run.

    Returns
    -------
    None or str
        If the executed code prints nothing, return None.
        Otherwise, return the printed output as a string.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or imports.
    """
    # Parse the code to check for malicious constructs
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    _check_ast(parsed)

    # Prepare a safe globals dictionary
    safe_globals = {
        '__builtins__': {name: getattr(builtins, name) for name in SAFE_BUILTINS}
    }

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<string>", mode="exec"), safe_globals)
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
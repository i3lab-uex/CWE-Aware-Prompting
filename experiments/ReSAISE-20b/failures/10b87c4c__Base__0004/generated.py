import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# List of AST node types that are disallowed in the submitted code
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # present only in Python 2
    ast.Call,          # we filter specific calls below
    ast.Attribute,
}

# Calls to these builtins/functions are considered unsafe
DISALLOWED_CALLS = {
    'open',
    'eval',
    'exec',
    'compile',
    'input',          # might read external data
    '__import__',
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a disallowed
    construct is found.
    """
    # Disallow imports entirely
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise ValueError("Import statements are not allowed.")

    # Disallow any function calls to unsafe builtins
    if isinstance(node, ast.Call):
        func = node.func
        # handle simple name calls like eval()
        if isinstance(func, ast.Name) and func.id in DISALLOWED_CALLS:
            raise ValueError(f"Use of '{func.id}' is disallowed.")
        # handle attribute calls like os.system()
        if isinstance(func, ast.Attribute):
            attr_name = func.attr
            if attr_name in DISALLOWED_CALLS:
                raise ValueError(f"Use of '{attr_name}' is disallowed.")
        # allow other calls (e.g., print, len)
    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def process_code_input(code_input: str) -> None | str:
    """
    Safely execute a small Python code snippet provided as a string.

    Parameters
    ----------
    code_input : str
        The Python source code to run.

    Returns
    -------
    None or str
        If the executed code produces any output on stdout, that output is
        returned as a string.  If there is no output, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations such as imports, eval,
        exec, open, or any other unsafe constructs.
    """
    # Parse the code to an AST
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}") from e

    # Inspect the AST for disallowed nodes/calls
    _check_ast(parsed)

    # Prepare a restricted global namespace
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
        # Add any other safe builtins you wish to expose
    }

    restricted_globals = {
        '__builtins__': safe_builtins,
    }

    # Capture stdout
    output = StringIO()
    try:
        with redirect_stdout(output):
            exec(compile(parsed, filename="<user_code>", mode="exec"),
                 restricted_globals,
                 None)
    except Exception as e:
        # Re‑raise as ValueError to keep a consistent error type
        raise ValueError(f"Execution error: {e}") from e

    result = output.getvalue()
    return result if result else None
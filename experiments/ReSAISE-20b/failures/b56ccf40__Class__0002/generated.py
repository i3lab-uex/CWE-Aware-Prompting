import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# Whitelisted builtin functions that are safe to expose to user code
SAFE_BUILTINS = {
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
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
}

# Nodes that are disallowed in the user script
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                 # Py2 only; harmless if not present
    ast.Call,                 # but we will filter calls to __import__ and builtins like open
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
)

# Functions that are disallowed even if they appear as calls
DISALLOWED_FUNCTIONS = {
    'open',
    '__import__',
    'eval',
    'exec',
    'compile',
    'input',
    'locals',
    'globals',
    '__build_class__',
}

def _is_disallowed(node: ast.AST) -> bool:
    """
    Recursively check whether a node or any of its children is disallowed.
    """
    if isinstance(node, DISALLOWED_NODES):
        # Import nodes are outright forbidden
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return True

        # Calls to forbidden functions
        if isinstance(node, ast.Call):
            func = node.func
            # Handle simple name calls (e.g., open())
            if isinstance(func, ast.Name) and func.id in DISALLOWED_FUNCTIONS:
                return True
            # Handle attribute calls (e.g., obj.open())
            if isinstance(func, ast.Attribute):
                attr = func.attr
                if attr in DISALLOWED_FUNCTIONS:
                    return True

        # Attribute accesses (e.g., obj.__dict__) are disallowed
        if isinstance(node, ast.Attribute):
            return True

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if _is_disallowed(child):
            return True
    return False

def process_user_code(code_submission: str) -> str | None:
    """
    Execute user-submitted Python code in a restricted environment.

    Parameters
    ----------
    code_submission : str
        The script to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains syntax errors or uses disallowed constructs.
    """
    # 1. Parse the source to catch syntax errors
    try:
        parsed = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # 2. Walk the AST to detect disallowed nodes
    if _is_disallowed(parsed):
        raise ValueError("User code contains forbidden operations.")

    # 3. Prepare a restricted globals dictionary
    safe_globals = {
        "__builtins__": SAFE_BUILTINS,
    }

    # 4. Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals, {})
    except Exception as exc:
        # Re‑raise as ValueError to keep a consistent exception type
        raise ValueError(f"Error executing user code: {exc}") from exc

    # 5. Return captured output if any
    out = output_io.getvalue()
    return out if out else None
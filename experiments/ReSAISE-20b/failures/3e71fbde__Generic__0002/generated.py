import ast
from contextlib import redirect_stdout
from io import StringIO

# List of AST node types that are disallowed in the snippet.
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only; kept for completeness
    ast.Call,          # we will inspect calls separately
)

# Disallowed function names that can perform unsafe operations.
DISALLOWED_CALLS = {
    "eval",
    "exec",
    "__import__",
    "open",  # file I/O
    "input",
    "os.system",
    "subprocess.Popen",
}

def _is_disallowed_call(node: ast.Call) -> bool:
    """
    Return True if the call node is to a disallowed function.
    Handles simple names and dotted attributes.
    """
    # Handle simple name: eval(...)
    if isinstance(node.func, ast.Name):
        return node.func.id in DISALLOWED_CALLS
    # Handle attribute: os.system(...)
    if isinstance(node.func, ast.Attribute):
        parts = []
        cur = node.func
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
            full_name = ".".join(reversed(parts))
            return full_name in DISALLOWED_CALLS
    return False

def _check_ast(tree: ast.AST):
    """
    Walk the AST and raise ValueError if any disallowed construct is found.
    """
    for node in ast.walk(tree):
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError(f"Import statements are disallowed: {ast.dump(node)}")
        # Disallow exec (Python 2) or other dangerous calls
        if isinstance(node, ast.Call):
            if _is_disallowed_call(node):
                raise ValueError(f"Disallowed function call: {ast.dump(node)}")

def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet in a restricted environment.
    
    Parameters
    ----------
    snippet : str
        The code to execute.

    Returns
    -------
    None or str
        If the snippet produces no output, returns None.  Otherwise,
        returns the captured stdout as a string (stripped of trailing newlines).

    Raises
    ------
    ValueError
        If the snippet attempts a disallowed operation.
    """
    # First, parse and check for safety
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    _check_ast(tree)

    # Prepare restricted globals and locals
    safe_globals = {"__builtins__": {}}
    safe_locals = {}

    # Capture stdout
    buf = StringIO()
    try:
        with redirect_stdout(buf):
            exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, safe_locals)
    except Exception as e:
        # Re-raise exceptions from user code unchanged
        raise

    output = buf.getvalue()
    return output if output else None
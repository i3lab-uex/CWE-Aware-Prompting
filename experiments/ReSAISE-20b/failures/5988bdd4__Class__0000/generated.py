import ast
import builtins
import io
import sys

# ------------------------------------------------------------------------------
# Helper: list of disallowed AST node types
FORBIDDEN_NODES = {
    ast.Import,          # import statements
    ast.ImportFrom,
    ast.Exec,            # exec() in Python 2 (kept for completeness)
    ast.Call,           # calls to unsafe functions
    ast.Attribute,      # attribute access (e.g., os.system)
    ast.Subscript,      # subscripts on objects that might be unsafe
    ast.Lambda,
}

# Map of allowed builtins (very small subset)
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
    'print': print,
    'range': range,
    'str': str,
    'sum': sum,
}

# ------------------------------------------------------------------------------
def _is_safe_call(node: ast.Call) -> bool:
    """
    Determine if a function call is safe. We only allow calls to builtins that
    are explicitly whitelisted in ALLOWED_BUILTINS.
    """
    # Function must be a Name and its id must be in ALLOWED_BUILTINS
    if isinstance(node.func, ast.Name):
        return node.func.id in ALLOWED_BUILTINS
    # Reject attribute calls (e.g., os.system)
    return False

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any forbidden construct
    is found.
    """
    for child in ast.iter_child_nodes(node):
        # Check node type
        if isinstance(child, tuple(FORBIDDEN_NODES)):
            raise ValueError(f"Forbidden operation: {type(child).__name__}")

        # Special handling for Call nodes
        if isinstance(child, ast.Call):
            if not _is_safe_call(child):
                raise ValueError(f"Disallowed function call: {ast.unparse(child)}")

        # Recursively check children
        _check_ast(child)

# ------------------------------------------------------------------------------
def run_python_snippet(snippet_string: str):
    """
    Execute a user-provided Python snippet in a highly restricted environment.

    Parameters
    ----------
    snippet_string : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression if it produces output; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    # Parse the code to ensure it is syntactically valid
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Check for disallowed constructs
    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    # Capture stdout
    old_stdout = sys.stdout
    stdout_capture = io.StringIO()
    try:
        sys.stdout = stdout_capture
        # Execute the code
        exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # Retrieve output
    output = stdout_capture.getvalue()
    return output if output else None

# ------------------------------------------------------------------------------
# Example usage (uncomment to test)
# if __name__ == "__main__":
#     code = "x = 5\nprint('Hello', x)\n"
#     print(run_python_snippet(code))
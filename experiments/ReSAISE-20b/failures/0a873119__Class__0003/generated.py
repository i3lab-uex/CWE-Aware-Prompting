import ast
from types import SimpleNamespace

# List of AST node types that are disallowed in user scripts
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # Calls are inspected further
    ast.Exec,          # exec is not a node in modern Python but kept for clarity
)

# Call names that are considered unsafe (e.g., os.system, eval, exec)
UNSAFE_CALLS = {
    'eval',
    'exec',
    'open',
    'compile',
    'input',
    'os.system',
    'subprocess.run',
    'subprocess.Popen',
    'sys.exit',
}

# Allowed builtins
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'dict': dict,
    'list': list,
    'set': set,
    'tuple': tuple,
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any disallowed node
    or unsafe call is found.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(child).__name__}")

        # Inspect Call nodes for unsafe function names
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple name calls (e.g., eval(...))
            if isinstance(func, ast.Name):
                func_name = func.id
            # Handle attribute calls (e.g., os.system(...))
            elif isinstance(func, ast.Attribute):
                # Resolve the full dotted name (e.g., os.system)
                parts = []
                cur = func
                while isinstance(cur, ast.Attribute):
                    parts.append(cur.attr)
                    cur = cur.value
                if isinstance(cur, ast.Name):
                    parts.append(cur.id)
                func_name = ".".join(reversed(parts))
            else:
                func_name = None

            if func_name in UNSAFE_CALLS:
                raise ValueError(f"Unsafe function call detected: {func_name}")

        _check_ast(child)

def safe_run_script(script_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The Python code submitted by the user.

    Returns
    -------
    Any
        Result of the executed script if an expression is present;
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or has invalid syntax.
    """
    # Parse and validate the AST
    try:
        parsed = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    _check_ast(parsed)

    # Prepare the sandboxed environment
    sandbox = SimpleNamespace()
    sandbox.__dict__.update(SAFE_BUILTINS)

    # Execute the script
    try:
        exec(compile(parsed, filename="<safe_script>", mode="exec"), sandbox.__dict__, {})
    except Exception as exc:
        raise ValueError(f"Script execution failed: {exc}") from None

    # Attempt to return the value of the last expression if it exists
    # (Python's exec doesn't provide a result; we rely on a convention)
    return getattr(sandbox, "__result__", None)

# Example usage:
if __name__ == "__main__":
    code = """
x = 5
y = 10
__result__ = x + y
"""
    print(safe_run_script(code))   # Output: 15
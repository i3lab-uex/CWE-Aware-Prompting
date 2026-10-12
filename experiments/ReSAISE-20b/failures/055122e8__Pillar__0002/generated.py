import ast

# A whitelist of safe built‑in functions that may be used by user code.
SAFE_BUILTINS = {
    'abs': abs,
    'sum': sum,
    'len': len,
    'min': min,
    'max': max,
    'pow': pow,
    'round': round,
    # You can extend this list with other harmless functions if desired.
}

# Nodes that are considered dangerous and must not appear in the user code.
PROHIBITED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                # exec() is not a node in Python 3, but kept for clarity
    ast.Call,                # we will allow calls only to whitelisted builtins
    ast.Attribute,           # disallow attribute access (e.g., os.system)
    ast.Subscript,           # prevent accessing modules or dangerous objects
)

def _is_safe_node(node):
    """
    Recursively check that the AST node does not contain any prohibited constructs.
    """
    # Reject Import statements
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return False

    # Reject attribute access (e.g., os.system)
    if isinstance(node, ast.Attribute):
        return False

    # Reject subscript access (e.g., os['system'])
    if isinstance(node, ast.Subscript):
        return False

    # Reject calls to non‑whitelisted builtins
    if isinstance(node, ast.Call):
        # Only allow calls to names that are in SAFE_BUILTINS
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                return False
        else:
            # Calls to attributes or other expressions are disallowed
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_python_script(python_code: str):
    """
    Execute a user‑supplied Python script in a sandboxed environment.

    Parameters
    ----------
    python_code : str
        The code to execute.

    Returns
    -------
    Any
        The result of the last expression in the script, or None if there is no
        expression that produces a value.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    try:
        # Parse the code into an AST to perform static analysis
        parsed = ast.parse(python_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Perform safety checks
    if not _is_safe_node(parsed):
        raise ValueError("Script contains prohibited operations.")

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # Execute the code
    exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals, safe_locals)

    # If the user code ends with an expression that assigns to a variable named
    # "_result", we return its value; otherwise, return None.
    # This is a simple convention to retrieve results from scripts.
    return safe_locals.get("_result")
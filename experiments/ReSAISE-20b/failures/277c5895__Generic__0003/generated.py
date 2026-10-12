import ast
from types import ModuleType

# Whitelist of safe built‑ins that can be exposed to the user code
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
    # Add more safe built‑ins as required
}

# Nodes that are disallowed in user code
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 legacy
    ast.Call,
    ast.Attribute,
    ast.Global,
    ast.Nonlocal,
)

# Function names that are considered unsafe when called
UNSAFE_CALLS = {
    'open',
    '__import__',
    'eval',
    'exec',
    'compile',
    'input',
    'os',  # accessing os module
    'sys',
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively walk the AST and ensure that only allowed constructs are present.
    """
    if isinstance(node, DISALLOWED_NODES):
        return False

    # Disallow function calls to unsafe names
    if isinstance(node, ast.Call):
        func = node.func
        # Handle simple name calls: e.g., open(...)
        if isinstance(func, ast.Name) and func.id in UNSAFE_CALLS:
            return False
        # Handle attribute calls: e.g., os.system(...)
        if isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Name) and func.value.id in UNSAFE_CALLS:
                return False

    # Disallow accessing dunder attributes (e.g., __dict__, __class__)
    if isinstance(node, ast.Attribute):
        if node.attr.startswith('__') and node.attr.endswith('__'):
            return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_user_code(submitted_code: str):
    """
    Execute user supplied Python code in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The user provided Python script.

    Returns
    -------
    Any
        The value of the variable named 'result' if it exists after execution,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    # Parse code to AST and check for syntax errors
    try:
        tree = ast.parse(submitted_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the code only contains safe constructs
    if not _is_safe(tree):
        raise ValueError("Prohibited or unsafe operations detected in the script.")

    # Prepare a sandboxed global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Execute the code
    try:
        exec(compile(tree, filename="<user_code>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # Return the value of 'result' if defined
    return sandbox_locals.get("result", None)
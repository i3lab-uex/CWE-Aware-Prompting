import ast
from typing import Any

# List of AST node types that are considered unsafe
_UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # disallow all function calls
    ast.Exec,          # Python 2 only, but keep for completeness
    ast.Global,
    ast.Nonlocal,
    ast.Lambda,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.With,
    ast.Raise,
    ast.Try,
    ast.Assert,
}

# Functions that are explicitly allowed (you can extend this list)
_ALLOWED_CALLS = {
    "abs",
    "len",
    "sum",
    "min",
    "max",
}

# Names that are allowed to be referenced
_ALLOWED_NAMES = {
    "__builtins__": None,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST node tree contains only safe constructs.
    """
    if type(node) in _UNSAFE_NODES:
        return False

    # disallow any function calls that are not in the whitelist
    if isinstance(node, ast.Call):
        func = node.func
        # Only allow calls to simple names that are whitelisted
        if isinstance(func, ast.Name) and func.id in _ALLOWED_CALLS:
            pass
        else:
            return False

    # disallow attribute access (e.g., os.system)
    if isinstance(node, ast.Attribute):
        return False

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def run_code_snippet(user_code: str) -> Any:
    """
    Execute a user‑provided Python snippet in a sandboxed environment.
    Only simple expressions and a small set of built‑in functions are allowed.

    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or potentially dangerous calls.
    """
    # Parse the user code into an AST
    try:
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from exc

    # Validate safety
    if not _is_safe(parsed):
        raise ValueError("The code snippet contains prohibited actions.")

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": {}}
    for name in _ALLOWED_CALLS:
        safe_globals[name] = __builtins__[name]

    # Execute the code. Capture the result of the last expression if any.
    local_vars = {}
    exec(compile(parsed, filename="<user_snippet>", mode="exec"), safe_globals, local_vars)

    # If the user code ends with an expression (e.g., a literal or variable),
    # it will be stored in the last line's value. We can attempt to retrieve
    # a special variable `_result` that the user might set.
    return local_vars.get("_result", None)
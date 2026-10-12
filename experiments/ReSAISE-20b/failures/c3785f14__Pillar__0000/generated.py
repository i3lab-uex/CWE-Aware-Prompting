import ast
import builtins
import sys
from contextlib import redirect_stdout, io

# --------------------------------------------------------------------------- #
# 1. Define a list of disallowed AST node types and names
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,                # will be checked for specific functions
}

DISALLOWED_NAMES = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",                 # avoid interactive input
}

# Disallowed built‑ins that should be removed from the globals dict
DISALLOWED_BUILTINS = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",
}

# --------------------------------------------------------------------------- #
def _check_safety(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any disallowed
    construct is detected.
    """
    for child in ast.walk(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")

        # Disallow calls to dangerous functions
        if isinstance(child, ast.Call):
            func = child.func
            # Handle attribute calls (e.g., os.system)
            if isinstance(func, ast.Attribute):
                name = func.attr
            elif isinstance(func, ast.Name):
                name = func.id
            else:
                continue

            if name in DISALLOWED_NAMES:
                raise ValueError(f"Use of `{name}` is not allowed.")

        # Disallow usage of forbidden names via Name nodes
        if isinstance(child, ast.Name):
            if child.id in DISALLOWED_NAMES:
                raise ValueError(f"Use of `{child.id}` is not allowed.")

# --------------------------------------------------------------------------- #
def evaluate_code_string(code_string: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    str | None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Parse and validate safety
    try:
        parsed = ast.parse(code_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    _check_safety(parsed)

    # 2. Prepare a restricted global namespace
    safe_globals = {
        "__builtins__": {k: v for k, v in builtins.__dict__.items()
                         if k not in DISALLOWED_BUILTINS}
    }

    # 3. Capture stdout
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(compile(parsed, filename="<string>", mode="exec"),
                 safe_globals,
                 {})
    except Exception as exc:
        # Re‑raise exceptions from the user code as ValueError
        raise ValueError(f"Execution error: {exc}") from None

    output = f.getvalue()
    return output if output else None
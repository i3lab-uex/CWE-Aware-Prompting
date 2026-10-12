import ast
from types import SimpleNamespace

# Allowed built‑in functions that are considered safe.
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "print": print,
}

# AST nodes that are explicitly disallowed.
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec is not a node in py3 but keep for completeness
    ast.Call,          # we will filter calls to unsafe functions below
    ast.Attribute,
}

# Functions that are considered unsafe if called.
UNSAFE_FUNCTIONS = {
    "eval",
    "exec",
    "compile",
    "__import__",
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a disallowed construct is found.
    """
    for child in ast.walk(node):
        # Reject import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are prohibited.")

        # Reject attribute access (e.g., os.system)
        if isinstance(child, ast.Attribute):
            raise ValueError("Attribute access is prohibited.")

        # Reject calls to unsafe built‑ins
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names: eval(), exec(), etc.
            if isinstance(func, ast.Name) and func.id in UNSAFE_FUNCTIONS:
                raise ValueError(f"Use of '{func.id}' is prohibited.")
            # Handle calls to __import__ via attribute or other forms
            if isinstance(func, ast.Attribute):
                raise ValueError("Attribute calls are prohibited.")

    # No disallowed nodes found
    return

def execute_user_code(submitted_code: str):
    """
    Execute a user‑provided Python script in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute.

    Returns
    -------
    Any
        The result of the last expression in the code, or None if there is none.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or invalid syntax.
    """
    # 1. Parse the code to catch syntax errors early
    try:
        parsed = ast.parse(submitted_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in submitted code: {exc}") from None

    # 2. Inspect the AST for prohibited constructs
    _check_ast(parsed)

    # 3. Prepare a safe execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # 4. Execute the code
    try:
        compiled = compile(parsed, filename="<user_code>", mode="exec")
        exec(compiled, exec_globals, exec_locals)
    except Exception as exc:
        # Re‑raise as ValueError to keep a uniform error type
        raise ValueError(f"Execution failed: {exc}") from None

    # 5. Return the value of the last expression if present
    # In exec mode, we cannot capture expressions directly. If user wants a value,
    # they should assign it to a known variable, e.g., 'result'.
    return exec_locals.get("result", None)
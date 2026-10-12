import ast
from types import SimpleNamespace

# List of AST node types that are considered unsafe.
_UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 only, kept for completeness
    ast.Call,           # function calls are generally unsafe
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.With,
    ast.AsyncWith,
    ast.For,
    ast.While,
    ast.Try,
    ast.Raise,
    ast.Delete,
    ast.Global,
    ast.Nonlocal,
    ast.Await,
}

# A whitelist of safe built‑ins that are allowed to be used.
_SAFE_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "chr",
    "complex",
    "dict",
    "float",
    "int",
    "len",
    "list",
    "max",
    "min",
    "pow",
    "range",
    "repr",
    "round",
    "str",
    "sum",
    "tuple",
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that a node tree contains only safe constructs.
    """
    if type(node) in _UNSAFE_NODES:
        return False

    # For Call nodes, ensure the function being called is a safe builtin.
    if isinstance(node, ast.Call):
        # Resolve the name of the function being called
        func = node.func
        if isinstance(func, ast.Name):
            if func.id not in _SAFE_BUILTINS:
                return False
        else:
            # Any other form of function call is disallowed (e.g. attribute access)
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def safe_run_script(script_code: str) -> object:
    """
    Execute a user supplied Python script in a sandboxed environment.
    Only safe, pure‑function calls and literals are allowed.

    Parameters
    ----------
    script_code : str
        The code to execute. It may contain expressions or statements.

    Returns
    -------
    object
        The value of the last expression in the script, or None if none.

    Raises
    ------
    ValueError
        If the code contains syntax errors or disallowed operations.
    """
    try:
        # Parse the source into an AST
        parsed = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from None

    # Validate the AST for unsafe nodes
    if not _is_safe(parsed):
        raise ValueError("Script contains prohibited operations")

    # Prepare a minimal, safe globals dict
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in _SAFE_BUILTINS}}
    safe_locals = SimpleNamespace()

    # Execute the script
    exec(compile(parsed, filename="<safe_script>", mode="exec"), safe_globals, safe_locals.__dict__)

    # Attempt to return the value of the last expression if it exists
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            try:
                return eval(compile(ast.Expression(body=node.value), filename="<safe_script>", mode="eval"),
                            safe_globals, safe_locals.__dict__)
            except Exception:
                # If evaluation fails, simply return None
                return None

    return None
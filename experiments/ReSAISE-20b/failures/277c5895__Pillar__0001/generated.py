import ast
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# 1. Define a set of AST node types that are considered dangerous or
#    unsupported in this sandbox.
# --------------------------------------------------------------------------- #
DISALLOWED_NODES = {
    ast.Import,          # `import` statements
    ast.ImportFrom,
    ast.Exec,            # Python 2 exec statement (not present in Py3)
    ast.Call,            # function calls are disallowed unless explicitly allowed
    ast.Attribute,       # accessing attributes like os.system
    ast.Subscript,       # subscript access (e.g. a[0])
}

# --------------------------------------------------------------------------- #
# 2. Define a whitelist of safe built‑in functions that the user is allowed
#    to use.  Anything else will be blocked.
# --------------------------------------------------------------------------- #
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
    # add more pure functions if required
}

# --------------------------------------------------------------------------- #
# 3. Helper function to walk the AST and reject disallowed nodes
# --------------------------------------------------------------------------- #
def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST. Raise ValueError if a disallowed node is found.
    For Call nodes we allow only calls to functions in SAFE_BUILTINS.
    """
    for child in ast.iter_child_nodes(node):
        # Reject disallowed node types outright
        if type(child) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed operation: {type(child).__name__}")

        # Handle function calls
        if isinstance(child, ast.Call):
            # Only allow calls to names that are in SAFE_BUILTINS
            if isinstance(child.func, ast.Name):
                func_name = child.func.id
                if func_name not in SAFE_BUILTINS:
                    raise ValueError(f"Calling function '{func_name}' is not permitted.")
            else:
                # Any other form of call (e.g. attribute access) is forbidden
                raise ValueError("Only direct calls to safe built‑ins are allowed.")

        # Recurse
        _validate_ast(child)

# --------------------------------------------------------------------------- #
# 4. The main sandboxed execution function
# --------------------------------------------------------------------------- #
def execute_user_code(submitted_code: str) -> Any:
    """
    Execute a user‑provided Python script in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The Python source code to execute.

    Returns
    -------
    Any
        The result of the last expression in the script, or None if no
        expression produces a value.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or is syntactically invalid.
    """
    # 4.1 Parse the code to an AST; this also validates syntax
    try:
        parsed = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # 4.2 Walk the AST and enforce security restrictions
    _validate_ast(parsed)

    # 4.3 Prepare a restricted globals dictionary
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    # Optionally allow a limited set of modules, e.g. math
    import math
    safe_globals['math'] = math

    # 4.4 Execute the code
    exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals)

    # 4.5 Try to return the value of the last expression if present
    # We look for an Expr node that is the last statement in the body.
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate that expression in the same safe environment
        last_expr = parsed.body[-1].value
        try:
            return eval(compile(ast.Expression(last_expr), filename="<user_code>", mode="eval"),
                        safe_globals)
        except Exception:
            # If evaluation fails, fall back to None
            return None

    return None
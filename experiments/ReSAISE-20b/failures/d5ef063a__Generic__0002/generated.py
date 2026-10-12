import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# --- Allowed nodes ----------------------------------------------------------
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Constant,           # literals
    ast.Str, ast.Num,       # legacy for older Python <3.8
    ast.List, ast.Tuple,
    ast.Dict, ast.Set,
    ast.Name,
    ast.Call,
    ast.Load,
    ast.BinOp, ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.USub, ast.UAdd,
}

# Allowed built‑in functions
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool',
    'chr', 'divmod', 'float', 'int', 'len',
    'max', 'min', 'pow', 'range', 'round',
    'str', 'sum', 'tuple', 'list', 'dict',
}

def _is_allowed_node(node: ast.AST) -> bool:
    """Recursively check that the node and all its children are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_allowed_node(child):
            return False
    return True

def _check_syntax_and_security(code: str) -> None:
    """Parse the code and raise ValueError if syntax or security rules are violated."""
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from exc

    if not _is_allowed_node(tree):
        raise ValueError("Prohibited or unsafe code detected")

    # Disallow imports, function/class definitions, etc.
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom,
                             ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef, ast.For, ast.While,
                             ast.With, ast.Try)):
            raise ValueError(f"Prohibited construct: {type(node).__name__}")

def restricted_run_code(run_code: str):
    """
    Execute a user supplied Python script in a highly restricted environment.

    Parameters
    ----------
    run_code : str
        The Python script to execute.

    Returns
    -------
    str or None
        Captured stdout output of the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    _check_syntax_and_security(run_code)

    # Prepare restricted globals
    safe_builtins = {name: getattr(builtins, name) for name in ALLOWED_BUILTINS}
    globals_dict = {"__builtins__": safe_builtins}

    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(run_code, globals_dict, {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    output = output_buffer.getvalue()
    return output if output else None
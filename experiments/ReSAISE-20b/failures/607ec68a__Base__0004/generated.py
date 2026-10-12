import ast
import sys
import io
from contextlib import redirect_stdout

# ------------------------------------------------------------------
# Whitelist of allowed AST node types.  Anything not in this list will
# raise a ValueError.
SAFE_NODES = {
    # Expressions
    ast.Module, ast.Expr, ast.Load,
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.Call, ast.Name, ast.Constant,
    ast.Attribute,

    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitAnd, ast.BitXor, ast.UAdd, ast.USub,

    # Comparators
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE,

    # Boolean ops
    ast.And, ast.Or,

    # Literals
    ast.Tuple, ast.List, ast.Dict, ast.Set,
}

# ------------------------------------------------------------------
# Allowed built‑in functions and modules.  We expose a very small set
# to avoid accidental misuse.
ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,
}

ALLOWED_MODULES = {
    # Modules that are safe and useful for simple scripts.
    'math': __import__('math'),
    'random': __import__('random'),
}

# ------------------------------------------------------------------
def _check_ast(node: ast.AST):
    """
    Recursively verify that every node in the AST is permitted.
    Raises ValueError if an illegal construct is found.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed AST node: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

# ------------------------------------------------------------------
def safe_run_script(code: str):
    """
    Execute a user supplied Python script in a sandboxed environment.
    Only the constructs listed in SAFE_NODES are permitted.  The script
    runs with a restricted set of built‑ins and modules.

    Parameters:
        code (str): Python source to execute

    Returns:
        str or None: Captured stdout if any, otherwise None.

    Raises:
        ValueError: If the script contains disallowed syntax or
                    attempts to use prohibited objects.
    """
    # 1. Parse the code and check for syntax errors
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # 2. Validate AST nodes
    _check_ast(parsed)

    # 3. Prepare a restricted globals dictionary
    sandbox_globals = {
        '__builtins__': ALLOWED_BUILTINS,
        **ALLOWED_MODULES,
    }

    # 4. Capture stdout
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            exec(compile(parsed, filename='<user_script>', mode='exec'), sandbox_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user script: {exc}") from None

    result = output.getvalue()
    return result if result else None
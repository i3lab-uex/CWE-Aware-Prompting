import ast
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# ----------------------------------------------------------------------
# Whitelist of safe AST node types
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.FloorDiv,
    ast.UAdd, ast.USub,
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.BoolOp,
    ast.And, ast.Or,
    ast.IfExp,
    ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.Subscript,
    ast.Index,  # Python <3.9
    ast.Slice,
    ast.NameConstant,
    ast.Str,  # Python <3.8
    ast.Num,  # Python <3.8
}

# Additional safe builtins that can be exposed to the script
SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
}

def _check_ast(node: ast.AST):
    """
    Recursively ensure that all nodes in the AST are part of SAFE_NODES.
    Raise ValueError if any forbidden node is encountered.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) not in SAFE_NODES:
            raise ValueError(f"Forbidden construct: {type(child).__name__}")
        _check_ast(child)

def execute_user_script(submitted_script: str):
    """
    Safely execute a user‑supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The code to execute.

    Returns
    -------
    str or None
        Captured standard output of the script, if any.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # 1. Parse the script and validate AST
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in submitted script: {e}")

    _check_ast(parsed)

    # 2. Prepare a restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # 3. Capture stdout (and stderr) safely
    out_stream = io.StringIO()
    err_stream = io.StringIO()

    try:
        with redirect_stdout(out_stream), redirect_stderr(err_stream):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 safe_globals,
                 safe_locals)
    except Exception as exc:
        # Re‑raise as ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from exc

    # 4. Return captured output, or None if nothing was printed
    output = out_stream.getvalue()
    return output.strip() if output else None
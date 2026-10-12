import ast
import sys
import types
from io import StringIO

# List of allowed AST node types for a very small safe subset
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Str,
    ast.Constant,          # Python 3.8+
    ast.Name,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.NameConstant,      # Python <3.8
    ast.Compare,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
    ast.USub, ast.UAdd,
}

# Allowed builtins
_ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,
}

def _is_safe(node: ast.AST) -> bool:
    """Recursively ensure all nodes are in the allowed set."""
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_user_script(submitted_script: str):
    """
    Execute a user provided Python script in a highly restricted environment.
    
    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    Any
        The result of the last expression in the script, or None if there is none.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed constructs.
    """
    # Parse and validate syntax
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    if not _is_safe(parsed):
        raise ValueError("Script contains forbidden operations or unsafe constructs")

    # Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': _ALLOWED_BUILTINS,
    }

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    sys.stdout = fake_out

    # Execute the script
    try:
        exec(typed_code := compile(parsed, '<user_script>', 'exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # Return captured output if any, otherwise None
    out_value = fake_out.getvalue()
    return out_value or None
import ast
import io
import sys
from types import SimpleNamespace

# List of allowed AST node types. Anything else will be considered unsafe.
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.Num,           # for Python <3.8
    ast.Str,           # for Python <3.8
    ast.Bytes,         # for Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.UnaryOp,
    ast.BinOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.Attribute,
    ast.Subscript,
    ast.Index,         # for Python <3.9
    ast.Slice,
    ast.ExtSlice,
    ast.IfExp,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.And, ast.Or, ast.Not,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Unary ops
    ast.UAdd, ast.USub,
}

# Allowed builtins: only those that are safe and needed for basic scripts.
_ALLOWED_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'complex': complex,
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
    'tuple': tuple,
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are allowed.
    """
    if type(node) not in _ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def execute_user_script(submitted_script: str) -> str | None:
    """
    Safely execute a user supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    str | None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden nodes or cannot be parsed.
    """
    # Parse the script to an AST, raising SyntaxError if invalid
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    # Validate the AST
    if not _is_safe_node(parsed):
        raise ValueError("User script contains forbidden operations")

    # Prepare restricted globals
    safe_globals = {
        "__builtins__": _ALLOWED_BUILTINS,
    }

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None
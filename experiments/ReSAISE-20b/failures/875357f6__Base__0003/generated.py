import ast
import io
import sys
from types import ModuleType

# List of builtins that are considered safe for user scripts.
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
}

# Allowed AST node types for a very small sandbox.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.keyword,          # for function call keyword args
    ast.Attribute,        # allow attribute access to builtins only
}

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if an
    unexpected node type is found.
    """
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, tuple(ALLOWED_NODES)):
            raise ValueError(f"Forbidden syntax: {type(child).__name__}")
        # Special check for attribute access – only allow builtin attributes
        if isinstance(child, ast.Attribute):
            # Disallow chained attribute access (e.g., os.system)
            if not isinstance(child.value, ast.Name):
                raise ValueError("Attribute access to non-name is forbidden")
            if child.value.id not in SAFE_BUILTINS:
                raise ValueError(f"Attribute access to '{child.value.id}' is forbidden")
        _check_ast(child)

def execute_user_script(submitted_script: str):
    """
    Safely execute a user-provided Python script.

    Parameters
    ----------
    submitted_script : str
        The code to execute.

    Returns
    -------
    str or None
        Captured stdout if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden syntax or a syntax error.
    """
    # Parse and validate AST
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Capture stdout
    old_stdout = sys.stdout
    captured = io.StringIO()
    try:
        sys.stdout = captured
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    return output if output else None
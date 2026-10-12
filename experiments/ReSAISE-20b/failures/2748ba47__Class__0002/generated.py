import ast
import builtins
import io
import sys
from types import ModuleType

# --------------------------------------------------------------------
# 1. Safe AST node whitelist
SAFE_NODES = {
    # Expressions
    ast.Module, ast.Expr, ast.Str, ast.Bytes, ast.Num, ast.Constant,
    # Containers
    ast.List, ast.Tuple, ast.Set, ast.Dict, ast.NameConstant,
    # Operations
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.UAdd, ast.USub, ast.Not,
    # Boolean literals
    ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
    # Variables and attributes
    ast.Name, ast.Load, ast.Attribute,
    # Function calls (restricted)
    ast.Call, ast.keyword,
}

# --------------------------------------------------------------------
# 2. Allowed built‑in functions
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'print': print,          # but we'll capture it
    'range': range,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

# --------------------------------------------------------------------
def _check_ast(node: ast.AST):
    """
    Recursively ensure all nodes are in the SAFE_NODES set.
    Raise ValueError on disallowed node types.
    """
    if type(node) not in SAFE_NODES:
        raise ValueError(f"Disallowed syntax: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def _compile_and_execute(code: str, globals_dict: dict) -> None:
    """
    Compile the user code and execute it in a restricted environment.
    Capture stdout to return as string.
    """
    # Compile
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # AST safety check
    _check_ast(parsed)

    # Compile to code object
    compiled = compile(parsed, filename='<user_script>', mode='exec')

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compiled, globals_dict)
    finally:
        sys.stdout = old_stdout

    return fake_out.getvalue()

# --------------------------------------------------------------------
def execute_user_code(script_to_execute: str):
    """
    Execute a user supplied Python script in a sandboxed environment.
    
    Parameters
    ----------
    script_to_execute : str
        The user supplied Python source code.

    Returns
    -------
    str | None
        Captured stdout if the script prints anything; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or built‑in usage.
    """
    # Build a restricted globals dictionary
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        # Provide a dummy module for 'print' that writes to stdout
    }

    output = _compile_and_execute(script_to_execute, sandbox_globals)
    return output if output else None
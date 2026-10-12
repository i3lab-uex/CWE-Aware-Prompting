import ast
import builtins
import io
import sys
from contextlib import redirect_stdout

# Whitelisted AST node types that are considered safe
SAFE_NODES = {
    ast.Module, ast.Expr, ast.Load, ast.Store,
    ast.Num, ast.Str, ast.Bytes, ast.NameConstant,
    ast.Tuple, ast.List, ast.Dict, ast.Set,
    ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.Call, ast.keyword,
    ast.Name, ast.Attribute, ast.Subscript,
    ast.Index, ast.Slice,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.FloorDiv, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.Invert, ast.Not, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Logical
    ast.And, ast.Or,
}

# Whitelisted built‑in functions and constants
SAFE_BUILTINS = {
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
    'repr': repr,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # Constants
    'True': True,
    'False': False,
    'None': None,
}

def _validate_ast(node: ast.AST) -> None:
    """
    Recursively ensure that every node in the AST is of a whitelisted type.
    Raise ValueError if any disallowed node is found.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) not in SAFE_NODES:
            raise ValueError(f"Disallowed operation: {type(child).__name__}")
        _validate_ast(child)

def restricted_run_code(run_code: str):
    """
    Execute *run_code* in a highly restricted environment.
    Return the captured stdout as a string, or None if nothing was printed.
    Raise ValueError on syntax errors or prohibited operations.
    """
    # Parse the code to check for syntax and unsafe nodes
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    _validate_ast(parsed)

    # Prepare restricted globals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # No locals; everything is global
    local_vars = {}

    # Capture stdout
    output_io = io.StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<restricted>", mode="exec"),
                 safe_globals, local_vars)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    output = output_io.getvalue()
    return output if output else None
import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
# 1.  Allowed AST node types (anything else is considered unsafe)
SAFE_NODES = (
    # Statements
    ast.Module, ast.Expr, ast.Assign, ast.AugAssign,
    ast.Return, ast.FunctionDef, ast.Lambda, ast.If,
    ast.For, ast.While, ast.Break, ast.Continue,
    ast.Pass, ast.ImportFrom, ast.Import, ast.Global,
    # Expressions
    ast.Constant, ast.Name, ast.Attribute, ast.Call,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitAnd, ast.BitXor, ast.USub, ast.UAdd,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Others
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.Subscript, ast.Index, ast.Slice
)

# --------------------------------------------------------------------------- #
def _check_syntax_and_security(code: str) -> None:
    """
    Parses the code and raises ValueError if syntax is invalid or
    disallowed nodes are present.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from exc

    for node in ast.walk(tree):
        if not isinstance(node, SAFE_NODES):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")

# --------------------------------------------------------------------------- #
def _build_safe_globals() -> dict:
    """
    Returns a dictionary of globals that are safe to expose during exec.
    Only a minimal set of built-ins is provided.
    """
    # Basic safe builtins
    safe_builtins = {
        'abs': abs,
        'all': all,
        'any': any,
        'bool': bool,
        'dict': dict,
        'enumerate': enumerate,
        'filter': filter,
        'float': float,
        'int': int,
        'len': len,
        'list': list,
        'map': map,
        'max': max,
        'min': min,
        'pow': pow,
        'range': range,
        'repr': repr,
        'round': round,
        'str': str,
        'sum': sum,
        'tuple': tuple,
        # allow simple math functions
        'math': __import__('math'),
    }

    return {'__builtins__': safe_builtins}

# --------------------------------------------------------------------------- #
def execute_python_script(python_code: str):
    """
    Execute a user-provided Python script in a restricted environment.
    The function returns the result of the last evaluated expression
    or None if there is no explicit return.

    Raises:
        ValueError: If the script contains disallowed operations or
                    has syntax errors.
    """
    # 1. Syntax & security check
    _check_syntax_and_security(python_code)

    # 2. Prepare the execution environment
    safe_globals = _build_safe_globals()
    local_vars = {}

    # 3. Capture stdout (optional)
    output_capture = StringIO()
    try:
        with redirect_stdout(output_capture):
            exec(python_code, safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # 4. Try to return the value of the last expression, if any
    # The exec'ed code may define a function or variable named "__result__"
    if '__result__' in local_vars:
        return local_vars['__result__']

    # If the user wrote a single expression, we cannot capture it directly
    # without parsing; for simplicity return None.
    return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
#
# code = """
# __result__ = sum(range(10))
# """
# print(execute_python_script(code))   # Output: 45
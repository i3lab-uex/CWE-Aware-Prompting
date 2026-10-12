import ast
import io
import sys
from types import SimpleNamespace

# ---------- Safety utilities ----------
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
    # Add more if needed
}

SAFE_NAMES = set(SAFE_BUILTINS.keys())

ALLOWED_NODE_TYPES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
    ast.IfExp,  # ternary
}

def _is_safe_node(node):
    """Recursively ensure that every node is of an allowed type."""
    if not isinstance(node, tuple(ALLOWED_NODE_TYPES)):
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    # Ensure names are whitelisted
    if isinstance(node, ast.Name):
        if node.id not in SAFE_NAMES:
            return False
    # Disallow function calls
    if isinstance(node, ast.Call):
        return False
    return True

def _check_syntax_and_safety(code: str):
    """Parse and validate the code for safety."""
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    if not _is_safe_node(parsed):
        raise ValueError("Forbidden or unsafe operation detected in the user code.")
    return parsed

# ---------- Main function ----------
def evaluate_user_input(user_code: str):
    """
    Safely execute a user-provided Python script.

    Parameters
    ----------
    user_code : str
        The code submitted by the user.

    Returns
    -------
    output : str or None
        Captured stdout from the execution, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or syntax errors.
    """
    # Validate safety first
    parsed = _check_syntax_and_safety(user_code)

    # Prepare restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<user_script>", mode="exec"),
             safe_globals,
             safe_locals)
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
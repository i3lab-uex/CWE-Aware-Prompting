import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# List of AST node types that are disallowed in user scripts.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec() is a statement in Python 2; keep for safety
    ast.Call,          # restrict function calls that could be dangerous
    ast.Attribute,
    ast.Subscript,
    ast.Assign,
    ast.AugAssign,
    ast.Delete,
    ast.With,
    ast.Try,
)

# A whitelist of safe built-in functions that can be used by the user script.
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
    'tuple': tuple,
    # add more safe builtins as required
}

def _check_ast(node: ast.AST):
    """
    Recursively inspect the AST to ensure no forbidden nodes or
    disallowed function calls are present.
    """
    for child in ast.iter_child_nodes(node):
        # Reject any forbidden node type
        if isinstance(child, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden construct: {type(child).__name__}")

        # Allow only whitelisted builtins in function calls
        if isinstance(child, ast.Call):
            func = child.func
            # Function names must be simple identifiers referring to whitelisted builtins
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Use of non‑whitelisted builtin '{func.id}'")
            else:
                # Any other form (attribute access, lambda etc.) is disallowed
                raise ValueError("Only simple calls to whitelisted builtins are allowed")

        # Recursively check deeper nodes
        _check_ast(child)

def execute_user_script(submitted_script: str):
    """
    Execute a user‑supplied Python script in a highly restricted environment.

    Parameters
    ----------
    submitted_script : str
        The Python source code supplied by the user.

    Returns
    -------
    str or None
        Captured standard output of the script if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or uses forbidden operations.
    """
    # Parse to ensure valid Python syntax
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Inspect AST for disallowed constructs
    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
    }

    # Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)
    except Exception as exc:
        # Propagate runtime errors as ValueError to keep API consistent
        raise ValueError(f"Runtime error in user script: {exc}") from None

    # Return captured output if non‑empty
    result = output_buffer.getvalue()
    return result or None

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     script = """
# for i in range(3):
#     print('Hello', i)
# """
#     print(execute_user_script(script))
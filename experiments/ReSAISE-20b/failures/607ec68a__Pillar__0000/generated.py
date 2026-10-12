import ast
import io
import sys
from contextlib import redirect_stdout

# --------------------------------------------------------------------------- #
#   Safe execution helper
# --------------------------------------------------------------------------- #

def _is_prohibited(node: ast.AST) -> bool:
    """
    Determine whether an AST node represents a prohibited operation.
    """
    # Disallow import statements
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return True

    # Disallow calls to dangerous built‑ins or functions
    if isinstance(node, ast.Call):
        # Function name is a simple identifier (e.g. open(...))
        if isinstance(node.func, ast.Name):
            if node.func.id in _FORBIDDEN_CALLS:
                return True
        # Function is an attribute access (e.g. os.system(...))
        if isinstance(node.func, ast.Attribute):
            # Resolve the base object name (e.g. os)
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id in _FORBIDDEN_MODULES:
                    return True

    # Disallow attribute access to forbidden modules (e.g. os.system)
    if isinstance(node, ast.Attribute):
        if isinstance(node.value, ast.Name) and node.value.id in _FORBIDDEN_MODULES:
            return True

    # Disallow usage of exec/eval/compile
    if isinstance(node, ast.Exec):
        return True

    return False


def _check_syntax_and_protection(code: str) -> None:
    """
    Parse the code and raise ValueError if it contains syntax errors or
    prohibited constructs.
    """
    try:
        tree = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from None

    for node in ast.walk(tree):
        if _is_prohibited(node):
            raise ValueError("Prohibited operation detected in the script.")


# --------------------------------------------------------------------------- #
#   Safe globals definition
# --------------------------------------------------------------------------- #

# Allow only a minimal set of built‑ins that are considered safe.
_ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    # add more safe built‑ins if needed
}

# Modules that are explicitly forbidden to be imported or accessed.
_FORBIDDEN_MODULES = {
    'os',
    'sys',
    'subprocess',
    'shutil',
    'pickle',
    'json',          # restrict JSON handling to avoid deserialization risks
    'importlib',
}

# Functions that are disallowed even if they are built‑ins.
_FORBIDDEN_CALLS = {
    'open',
    'exec',
    'eval',
    'compile',
    '__import__',
    'input',
}

# --------------------------------------------------------------------------- #
#   Public API
# --------------------------------------------------------------------------- #

def safe_run_script(code: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    code : str
        The user's Python source code to execute.

    Returns
    -------
    str | None
        Captured stdout output if any; otherwise, None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or has syntax errors.
    """
    # 1. Validate syntax and disallowed constructs
    _check_syntax_and_protection(code)

    # 2. Prepare restricted execution environment
    exec_globals = {'__builtins__': _ALLOWED_BUILTINS}
    exec_locals = {}

    # 3. Capture stdout
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(code, exec_globals, exec_locals)
    except Exception as exc:
        # Wrap runtime errors into ValueError to keep the API consistent
        raise ValueError(f"Execution error: {exc}") from None

    # 4. Return captured output if any
    result = output_buffer.getvalue()
    return result or None

# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     user_code = """
#     for i in range(3):
#         print("Hello", i)
#     """
#     print(safe_run_script(user_code))
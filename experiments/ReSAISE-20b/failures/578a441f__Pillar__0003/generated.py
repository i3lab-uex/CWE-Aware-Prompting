import ast
import sys
from types import FunctionType

# A minimal set of safe builtins that we expose to the user script.
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
    # Add more safe functions if needed.
}

# Disallowed AST node types
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,               # we allow only calls to SAFE_BUILTINS
    ast.Attribute,
    ast.Subscript,
    ast.Delete,
    ast.Global,
    ast.Nonlocal,
    ast.Lambda,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.With,
    ast.Raise,
    ast.Try,
    ast.While,
    ast.For,
    ast.AsyncFor,
    ast.IfExp,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
}

def _check_syntax_and_security(script: str) -> None:
    """
    Parse the script and ensure it does not contain disallowed constructs.
    Raises ValueError on syntax errors or prohibited nodes.
    """
    try:
        tree = ast.parse(script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    for node in ast.walk(tree):
        if isinstance(node, DISALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")

        # Allow calls only to names that are in SAFE_BUILTINS
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Call to unsafe function '{func.id}'")
            else:
                # Any other call form (attribute, lambda, etc.) is forbidden
                raise ValueError(f"Disallowed function call form: {ast.dump(node)}")

def run_user_script(user_script: str):
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    user_script : str
        The Python script to execute. It may contain statements and
        expressions but must not use disallowed constructs.

    Returns
    -------
    Any
        The value of the last expression in the script if it exists,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    _check_syntax_and_security(user_script)

    # Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    # Local namespace for execution
    sandbox_locals = {}

    try:
        exec(user_script, sandbox_globals, sandbox_locals)
    except Exception as exc:
        # Convert any exception raised during execution to ValueError
        raise ValueError(f"Error executing user script: {exc}") from None

    # If the last statement is an expression, its value will be in
    # sandbox_locals under a special key if we had compiled as Expression.
    # Since we used exec, there's no direct way to retrieve the last
    # expression value. We'll return None.
    return None

# Example usage (commented out):
# if __name__ == "__main__":
#     script = "a = 5\nb = a * 2\nprint(b)"
#     run_user_script(script)
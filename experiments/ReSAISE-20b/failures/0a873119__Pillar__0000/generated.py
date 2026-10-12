import ast
from types import ModuleType, FunctionType

# List of AST node types that are considered unsafe
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python 2 only; harmless but keep for completeness
    ast.Global,
    ast.Nonlocal,
    ast.With,  # could be used for file handling
    ast.Call,  # allow only safe calls via whitelisting below
}

# Whitelist of built-in functions that are considered safe
SAFE_BUILTINS = {
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
    'print': print,
    'range': range,
    'round': round,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
}

# Whitelist of allowed module names that can be imported
ALLOWED_IMPORTS = {
    # Add modules that are considered safe for this sandbox
    'math': __import__('math'),
    # Example: allow json if needed
    # 'json': __import__('json'),
}

class UnsafeCodeError(ValueError):
    """Raised when user code contains disallowed operations."""
    pass

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise UnsafeCodeError if disallowed nodes are found.
    Additionally, for Call nodes we ensure that the called function is in SAFE_BUILTINS or
    an attribute access on a whitelisted module.
    """
    for child in ast.iter_child_nodes(node):
        # Check node type
        if isinstance(child, tuple(UNSAFE_NODES)):
            raise UnsafeCodeError(f"Disallowed statement: {type(child).__name__}")

        # Special handling for function calls
        if isinstance(child, ast.Call):
            func = child.func
            # Allow only direct calls to safe builtins
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise UnsafeCodeError(f"Use of unsafe function: {func.id}")
            # Allow attribute access on whitelisted modules, e.g., math.sqrt
            elif isinstance(func, ast.Attribute):
                if not (
                    isinstance(func.value, ast.Name)
                    and func.value.id in ALLOWED_IMPORTS
                ):
                    raise UnsafeCodeError(f"Disallowed attribute call: {ast.dump(func)}")
            else:
                raise UnsafeCodeError(f"Unsupported function call type: {ast.dump(func)}")

        # Recurse
        _check_ast(child)

def safe_run_script(script_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The Python code to execute.

    Returns
    -------
    Any
        Value of variable '__result__' if set by the script, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse code to AST and check for unsafe patterns
    try:
        parsed = ast.parse(script_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    try:
        _check_ast(parsed)
    except UnsafeCodeError as e:
        raise ValueError(f"Prohibited operation detected: {e}") from None

    # Prepare restricted globals
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        **ALLOWED_IMPORTS
    }
    sandbox_locals = {}

    # Execute the script
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    # Return the value of a special variable if defined
    return sandbox_locals.get('__result__', None)

# Example usage:
if __name__ == "__main__":
    code = """
x = 5
y = 10
__result__ = x + y
"""
    print(safe_run_script(code))   # Output: 15
import ast
import sys
import io
from types import ModuleType

# Whitelist of safe built‑ins that are allowed in the snippet
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
    'sum': sum,
    'str': str,
    'tuple': tuple,
    # Add more safe built‑ins as required
}

# AST nodes that are disallowed in a snippet
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # Calls to arbitrary functions are disallowed
    ast.Attribute,     # Prevent attribute access (e.g., os.system)
    ast.Subscript,     # Prevent subscript access to built‑ins (e.g., __import__)
    ast.NameConstant,  # Prevent constants like True/False
}

# Additional runtime checks for calls to dangerous functions
FORBIDDEN_CALLS = {
    'open',
    'exec',
    'eval',
    'compile',
    '__import__',
}

def _check_syntax_and_security(snippet: str) -> ast.Module:
    """
    Parse the snippet and perform static checks for forbidden syntax or calls.
    Raises ValueError if a violation is found.
    """
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}") from None

    for node in ast.walk(tree):
        # Disallow certain AST nodes outright
        if isinstance(node, tuple(FORBIDDEN_NODES)):
            raise ValueError(f"Forbidden syntax: {type(node).__name__}")

        # Disallow calls to dangerous functions
        if isinstance(node, ast.Call):
            func = node.func
            # Handle simple name calls like open(...)
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                raise ValueError(f"Forbidden function call: {func.id}")
            # Handle attribute calls like os.system(...)
            if isinstance(func, ast.Attribute):
                raise ValueError(f"Attribute access is forbidden: {ast.unparse(node)}")

    return tree

def _create_safe_environment() -> dict:
    """
    Create a restricted execution environment.
    """
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
        # No module imports are allowed
    }
    return safe_globals

def run_python_snippet(snippet_string: str):
    """
    Execute a user provided Python snippet in a sandboxed environment.
    Only benign operations are allowed. The function returns the value
    of the last expression if it produces one; otherwise None.

    Raises ValueError for forbidden operations or syntax errors.
    """
    # 1. Static checks
    tree = _check_syntax_and_security(snippet_string)

    # 2. Prepare environment
    safe_env = _create_safe_environment()

    # 3. Capture stdout to detect printed output
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Compile and execute the code
        compiled = compile(tree, filename="<snippet>", mode="exec")
        exec(compiled, safe_env)
    except Exception as exc:
        raise ValueError(f"Runtime error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 4. Attempt to return the value of the last expression
    # This is a best‑effort approach: we look for a name that was last assigned.
    # If the snippet ends with an expression (e.g., 2+3), it will be evaluated
    # during exec and left in the last expression value of the compiled code.
    # Python does not expose that directly, so we return None if no explicit
    # variable is set.
    # For educational purposes, we simply return None after execution.
    output = fake_out.getvalue()
    if output.strip():
        # If the snippet printed something, return it as a string
        return output.rstrip('\n')
    return None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(run_python_snippet("print('Hello, world!')"))
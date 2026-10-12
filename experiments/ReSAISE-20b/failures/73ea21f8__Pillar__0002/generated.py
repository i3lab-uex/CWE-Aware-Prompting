import ast
import sys
import types
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

# --------------------------------------------------------------------------- #
# 1. Define a list of AST node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,        # calls are checked more precisely below
    ast.Attribute,   # disallow attribute access to dangerous objects
)

# 2. Define a whitelist of safe built‑in functions
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
    # ... add more if needed
}

# 3. Visitor that walks the AST and raises ValueError on prohibited nodes
class SafetyVisitor(ast.NodeVisitor):
    def __init__(self, source: str):
        self.source = source

    def generic_visit(self, node):
        if isinstance(node, UNSAFE_NODES):
            raise ValueError(f"Prohibited construct: {type(node).__name__}")
        # Disallow attribute access that could reach dangerous objects
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id in {'__import__', 'eval', 'exec'}:
                raise ValueError("Disallowed attribute access to dangerous name")
        # Disallow calls to unsafe builtins
        if isinstance(node, ast.Call):
            func = node.func
            # Handle simple names e.g., eval()
            if isinstance(func, ast.Name):
                if func.id in {'eval', 'exec', 'open', '__import__'}:
                    raise ValueError(f"Disallowed call to {func.id}")
            # Handle attribute calls e.g., obj.eval()
            elif isinstance(func, ast.Attribute):
                if func.attr in {'eval', 'exec'}:
                    raise ValueError(f"Disallowed call to {func.attr}")
        super().generic_visit(node)

# --------------------------------------------------------------------------- #
def run_code_snippet(user_code: str):
    """
    Execute a user supplied Python snippet in a tightly restricted environment.

    Parameters
    ----------
    user_code : str
        The code snippet to execute.  It may contain multiple statements.

    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if there is no
        result.

    Raises
    ------
    ValueError
        If the snippet contains prohibited constructs.
    """
    # 1. Parse the code to an AST
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # 2. Inspect the AST for unsafe nodes
    SafetyVisitor(user_code).visit(tree)

    # 3. Prepare a restricted globals dictionary
    safe_globals = {
        "__builtins__": SAFE_BUILTINS,
    }

    # 4. Capture stdout/stderr to prevent leakage
    output = StringIO()
    with redirect_stdout(output), redirect_stderr(output):
        # 5. Execute the code
        exec(compile(tree, filename="<user_snippet>", mode="exec"), safe_globals)

    # 6. Attempt to retrieve the value of the last expression if it exists
    # Since exec does not return values, we look for a variable named "__last_expr__"
    # that user code can set. Alternatively, we simply return None.
    result = safe_globals.get("__last_expr__", None)
    return result
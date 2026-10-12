import ast
import sys
import io
from contextlib import redirect_stdout

# List of AST node types that are considered unsafe
_FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls to builtins like __import__ etc.
    ast.Attribute,     # attribute access can be dangerous
    ast.Subscript,
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
    ast.With,
    ast.Raise,
    ast.Try,
    ast.ExceptHandler,
    ast.AugAssign,
    ast.Delete,
    ast.Exec,          # Python 2 only
}

# Builtins that are not allowed to be called
_FORBIDDEN_BUILTINS = {
    'open', 'eval', 'exec', '__import__',
    'compile', 'input', 'dir', 'locals',
    'vars', 'globals', 'getattr', 'setattr',
    'delattr', 'help', 'quit', 'exit',
}

class _SafetyVisitor(ast.NodeVisitor):
    def visit(self, node):
        if type(node) in _FORBIDDEN_NODES:
            raise ValueError(f"Forbidden syntax: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Disallow calls to forbidden builtins
        if isinstance(node.func, ast.Name) and node.func.id in _FORBIDDEN_BUILTINS:
            raise ValueError(f"Forbidden builtin call: {node.func.id}")
        self.generic_visit(node)

def run_python_snippet(snippet_string: str):
    """
    Execute a user‑supplied Python snippet in a restricted environment.
    
    Parameters
    ----------
    snippet_string : str
        The code to execute.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden syntax, imports, or builtin calls,
        or if it fails to compile.
    """
    # 1. Parse and validate the syntax
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # 2. Walk the AST to detect unsafe constructs
    _SafetyVisitor().visit(parsed)

    # 3. Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': {
            # expose only a minimal set of safe builtins
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
            'print': print,          # allow printing
            'range': range,
            'str': str,
            'sum': sum,
        }
    }

    # 4. Capture stdout to return printed output if needed
    stdout_capture = io.StringIO()
    try:
        with redirect_stdout(stdout_capture):
            exec(compile(parsed, filename='<snippet>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # 5. If the snippet produced a value via expression, return it
    #    (Python exec does not give us the last value directly; we can
    #     request a special variable `__result__` that user code may set)
    result = safe_globals.get('__result__', None)

    # 6. If nothing was returned but there is printed output, return that string
    out = stdout_capture.getvalue()
    if result is None and out:
        return out.rstrip('\n')

    return result
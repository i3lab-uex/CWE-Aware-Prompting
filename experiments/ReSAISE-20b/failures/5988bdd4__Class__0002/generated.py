import ast
import builtins
from contextlib import redirect_stdout
import io

# Whitelist of safe built‑in functions / types
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
    'print': print,
    'range': range,
    'round': round,
    'sum': sum,
    'tuple': tuple,
    'str': str,
    'repr': repr,
    # add more safe built‑ins if needed
}

# AST visitor that rejects disallowed constructs
class SafeVisitor(ast.NodeVisitor):
    FORBIDDEN_NODES = (
        ast.Import, ast.ImportFrom,
        ast.Exec,  # Python 2
        ast.Call,  # we allow only safe calls via whitelist
        ast.Attribute,
        ast.Subscript,
        ast.Lambda,
        ast.Global, ast.Nonlocal,
        ast.With,
        ast.Try,
        ast.Raise,
    )

    def generic_visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden construct: {type(node).__name__}")
        # Disallow calls to arbitrary functions
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Call to unsafe function: {func.id}")
            else:
                # Any other call form is disallowed
                raise ValueError("Only simple function calls to whitelisted built‑ins are allowed")
        super().generic_visit(node)

def run_python_snippet(snippet_string: str):
    """
    Execute a user supplied Python snippet in a safe sandbox.

    Parameters
    ----------
    snippet_string : str
        The code to execute. Only simple expressions and statements that use the
        whitelisted built‑ins are permitted.

    Returns
    -------
    Any
        The value of the last expression in the snippet, if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    # Parse and validate the code
    try:
        tree = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Ensure the snippet contains no disallowed constructs
    SafeVisitor().visit(tree)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Capture stdout to prevent leakage
    stdout_buffer = io.StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(tree, filename="<snippet>", mode="exec"), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # Attempt to return the value of the last expression if present
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        # Evaluate the expression in the same environment
        expr_code = compile(ast.Expression(tree.body[-1].value), filename="<expr>", mode="eval")
        return eval(expr_code, exec_globals, exec_locals)

    # If there is no expression or nothing produced, return None
    return None
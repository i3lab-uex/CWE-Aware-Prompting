import ast
import builtins
import sys
import io
from contextlib import redirect_stdout

# Whitelisted builtin functions that are considered safe.
SAFE_BUILTINS = {
    'print': builtins.print,
    'len': builtins.len,
    'range': builtins.range,
    'abs': builtins.abs,
    'min': builtins.min,
    'max': builtins.max,
    'sum': builtins.sum,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    # Add more safe functions as needed
}

# Node visitor to detect disallowed syntax.
class SafeNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.forbidden_nodes = {
            ast.Import, ast.ImportFrom,  # disallow imports
            ast.Exec,                     # exec is removed in Py3 but kept for completeness
            ast.Call,
            ast.Name,                     # allow names only if in SAFE_BUILTINS or local vars
        }

    def generic_visit(self, node):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValueError("Import statements are forbidden.")
        if isinstance(node, ast.Call):
            # Allow calls only to safe builtins
            func = node.func
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Call to forbidden function '{func.id}'.")
            elif isinstance(func, ast.Attribute):
                raise ValueError("Attribute access is forbidden.")
        if isinstance(node, ast.Name):
            # Names are allowed; resolution will happen at runtime
            pass
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is forbidden.")
        if isinstance(node, ast.Lambda):
            raise ValueError("Lambda expressions are forbidden.")
        super().generic_visit(node)

def process_python_code(code_str: str):
    """
    Execute a snippet of Python code safely.

    Parameters
    ----------
    code_str : str
        User supplied Python code.

    Returns
    -------
    Any
        The value of the last expression in the snippet if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or calls.
    """
    # First, parse the code to check for syntax errors
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Verify that the syntax is safe
    SafeNodeVisitor().visit(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Capture local variables
    safe_locals = {}

    # Determine if the last node is an expression to return its value
    last_expr_value = None
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression separately
        expr_code = compile(ast.Expression(parsed.body[-1].value), '<string>', 'eval')
    else:
        expr_code = None

    # Compile the rest of the code
    exec_body = parsed.body[:-1] if expr_code else parsed.body
    exec_source = ast.Module(body=exec_body, type_ignores=[])
    compiled_exec = compile(exec_source, '<string>', 'exec')

    # Execute with stdout redirected to capture prints
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            exec(compiled_exec, safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # If there was an expression, evaluate it
    if expr_code:
        try:
            last_expr_value = eval(expr_code, safe_globals, safe_locals)
        except Exception as exc:
            raise ValueError(f"Expression evaluation error: {exc}") from exc

    # Optionally, you could return the captured stdout as well
    return last_expr_value
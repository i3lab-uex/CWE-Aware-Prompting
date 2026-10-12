import ast
import io
import sys
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# Safe execution environment
# --------------------------------------------------------------------------- #

# Whitelisted builtins – keep only a very small subset
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
    # add more as needed
}

# --------------------------------------------------------------------------- #
# AST visitor that checks for disallowed constructs
# --------------------------------------------------------------------------- #

class DisallowVisitor(ast.NodeVisitor):
    """
    Visits an AST and raises ValueError if it contains disallowed nodes.
    """

    FORBIDDEN_NAMES = {
        # Builtins that can be dangerous
        'open', 'eval', 'exec', '__import__',
        # Common system calls
        'system', 'popen', 'spawn', 'fork',
    }

    def visit_Import(self, node: ast.Import):
        raise ValueError("Import statements are forbidden")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Import statements are forbidden")

    def visit_Call(self, node: ast.Call):
        # Check function name
        func = node.func
        if isinstance(func, ast.Name) and func.id in self.FORBIDDEN_NAMES:
            raise ValueError(f"Call to forbidden function '{func.id}'")
        # Recursively visit arguments
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent attribute access that could reach dangerous modules
        if isinstance(node.value, ast.Name) and node.value.id in ('os', 'sys', 'subprocess'):
            raise ValueError(f"Attribute access to '{node.value.id}' is forbidden")
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        raise ValueError("Global statements are forbidden")

    def visit_Nonlocal(self, node: ast.Nonlocal):
        raise ValueError("Nonlocal statements are forbidden")

    def visit_Exec(self, node: ast.Exec):
        raise ValueError("Exec statements are forbidden")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Import statements are forbidden")

    def visit_Expr(self, node: ast.Expr):
        self.generic_visit(node)

    # All other nodes are allowed; use generic_visit to continue

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def process_python_code(code_str: str) -> Optional[Any]:
    """
    Execute a user supplied Python code string in a sandboxed environment.

    Parameters
    ----------
    code_str : str
        The Python code snippet to execute.

    Returns
    -------
    Any or None
        The value of the last expression if present; otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or invalid syntax.
    """
    # 1. Parse and validate AST
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # Run disallow visitor
    DisallowVisitor().visit(parsed)

    # 2. Separate statements and last expression (if any)
    body = parsed.body
    if not body:
        return None

    # If the last node is an expression, evaluate it separately
    last_expr = body[-1] if isinstance(body[-1], ast.Expr) else None

    exec_body = body[:-1] if last_expr is not None else body

    # Compile statements
    exec_code = ast.Module(body=exec_body, type_ignores=[])
    compiled_exec = compile(exec_code, filename='<sandbox>', mode='exec')

    # Prepare environment
    local_ns = {}
    global_ns = {'__builtins__': SAFE_BUILTINS}

    # 3. Capture stdout
    old_stdout = sys.stdout
    try:
        out_capture = io.StringIO()
        sys.stdout = out_capture

        # Execute statements
        exec(compiled_exec, global_ns, local_ns)

        # Evaluate last expression if present
        result = None
        if last_expr is not None:
            expr_code = ast.Expression(body=last_expr.value)
            compiled_expr = compile(expr_code, filename='<sandbox>', mode='eval')
            result = eval(compiled_expr, global_ns, local_ns)

        # Optionally return captured output if needed
        # For this implementation we ignore stdout content

    finally:
        sys.stdout = old_stdout

    return result
import ast
import io
import sys
from types import SimpleNamespace

# ----------------------------------------------------------------------
# AST visitor that rejects disallowed nodes.
# ----------------------------------------------------------------------
class SafeNodeVisitor(ast.NodeVisitor):
    """Ensure the user code does not contain unsafe constructs."""

    # Nodes that are explicitly forbidden
    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,                # Python 2 only – keep for completeness
        ast.Call,
    )

    # Call names that are considered dangerous
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'open',
        '__import__', 'compile', 'input',
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Reject calls to dangerous functions
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_CALLS:
            raise ValueError(f"Forbidden function call: {node.func.id}")
        self.generic_visit(node)


def evaluate_user_input(user_code: str):
    """
    Safely execute a small user supplied Python script.

    Parameters
    ----------
    user_code : str
        The code submitted by the user.

    Returns
    -------
    str | None
        Whatever was printed to stdout, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains syntax errors or disallowed operations.
    """
    # 1. Syntax check and safety validation
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Validate the AST
    SafeNodeVisitor().visit(parsed)

    # 2. Prepare a restricted execution environment
    safe_builtins = {
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'len': len,
        'range': range,
        'print': print,           # allow printing
    }
    exec_globals = {'__builtins__': safe_builtins}
    exec_locals = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename='<user_code>', mode='exec'), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
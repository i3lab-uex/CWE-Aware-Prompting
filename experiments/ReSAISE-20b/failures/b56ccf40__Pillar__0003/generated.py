import ast
import io
import sys

# A list of safe built‑in functions that can be used by user code.
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'sorted': sorted,
    # add more as needed
}

# Nodes that are disallowed in the user script.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec statement (Python 2)
    ast.Global,        # global statements
    ast.Nonlocal,      # nonlocal statements
    ast.With,          # with statements (can hide side effects)
)

# Names that are disallowed even if they come from builtins.
FORBIDDEN_NAMES = {
    'open',
    'eval',
    'exec',
    '__import__',
    'compile',
    'input',
    'os',            # module names
    'sys',
    'subprocess',
}

class SafeVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if forbidden nodes or names are found.
    """
    def visit(self, node):
        # Reject any forbidden node types
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden statement: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, (ast.Load, ast.Store)) and node.id in FORBIDDEN_NAMES:
            raise ValueError(f"Forbidden identifier: {node.id}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Reject calls to forbidden functions
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
            raise ValueError(f"Forbidden function call: {node.func.id}")
        super().visit(node)

def process_user_code(code_submission: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    code_submission : str
        The user supplied Python source code.

    Returns
    -------
    output : str or None
        Captured standard output from the script, if any.  If the script does not
        produce output, returns None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed constructs.
    """
    # 1. Parse and validate syntax
    try:
        parsed = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # 2. Walk the AST to ensure only safe constructs are used
    SafeVisitor().visit(parsed)

    # 3. Prepare a sandboxed environment
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        # Optionally, expose an empty dict for locals
    }

    # 4. Capture stdout
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    try:
        sys.stdout = captured_output
        exec(compile(parsed, filename='<user_script>', mode='exec'), sandbox_globals)
    except Exception as exc:
        # Re‑raise any exception from user code as ValueError
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = captured_output.getvalue()
    return output if output else None
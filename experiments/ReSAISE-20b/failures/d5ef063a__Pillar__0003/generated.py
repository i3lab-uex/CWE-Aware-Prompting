import ast
import io
import sys
from types import ModuleType

# Allowed built-in functions and names
ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
}

# Names that are prohibited in the script
PROHIBITED_NAMES = {
    'open', 'exec', 'eval', 'compile',
    '__import__', 'input', 'locals', 'globals',
    'dir', 'vars', 'getattr', 'setattr',
    '__builtins__', 'exit', 'quit',
}

# Prohibited AST node types
PROHIBITED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls are filtered by name later
    ast.Attribute,     # e.g., os.system
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.For,
    ast.While,
    ast.Global,
    ast.Nonlocal,
)

class SafeVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if a prohibited node or name is found.
    """
    def visit(self, node):
        if isinstance(node, PROHIBITED_NODES):
            raise ValueError(f"Prohibited statement: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node: ast.Name):
        if node.id in PROHIBITED_NAMES:
            raise ValueError(f"Use of prohibited name: {node.id}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Allow calls only to allowed builtins
        if isinstance(node.func, ast.Name) and node.func.id not in ALLOWED_BUILTINS:
            raise ValueError(f"Call to disallowed function: {node.func.id}")
        super().visit(node)

def restricted_run_code(run_code: str):
    """
    Execute user-provided Python code in a sandboxed environment.

    Parameters
    ----------
    run_code : str
        The Python script to execute.

    Returns
    -------
    str | None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains prohibited actions or syntax errors.
    """
    # Parse and validate syntax
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from None

    # Perform static checks
    SafeVisitor().visit(parsed)

    # Prepare safe execution environment
    safe_globals = {'__builtins__': ALLOWED_BUILTINS}
    safe_locals: dict = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<restricted>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
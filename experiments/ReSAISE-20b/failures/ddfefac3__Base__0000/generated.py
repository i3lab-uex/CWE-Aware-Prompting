import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# ------------------------------------------------------------------------------
# Helper: whitelist of safe built‑in functions / constants
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
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
    'tuple': tuple,
    'zip': zip,
    # I/O helpers
    'print': print,
}

# ------------------------------------------------------------------------------
class ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any forbidden node is encountered.
    Forbidden nodes:
      - Import / ImportFrom
      - Exec, Eval, Call to eval/exec (via ast.Name)
      - Call to open()
      - Attribute access on arbitrary objects (to prevent e.g. __import__)
    """
    FORBIDDEN_NAMES = {'__import__', 'eval', 'exec', 'open'}

    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_Call(self, node):
        # Detect calls to eval, exec or open by name
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_NAMES:
            raise ValueError(f"Use of '{node.func.id}' is forbidden")
        # Detect attribute calls like obj.__dict__ etc.
        if isinstance(node.func, ast.Attribute):
            # disallow any attribute call on a name that is not explicitly allowed
            if isinstance(node.func.value, ast.Name):
                attr_name = node.func.attr
                # allow only a very small set of safe attributes (e.g., .items for dict)
                if attr_name not in {'items', 'keys', 'values'}:
                    raise ValueError(f"Attribute access '{attr_name}' is forbidden")
        self.generic_visit(node)

    def visit_Exec(self, node):
        raise ValueError("exec statements are not allowed")

    def visit_Name(self, node):
        # Disallow use of dangerous names
        if node.id in self.FORBIDDEN_NAMES:
            raise ValueError(f"Use of '{node.id}' is forbidden")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow attribute access that could lead to code injection
        if isinstance(node.value, ast.Name):
            # e.g., __class__ or __dict__
            if node.attr.startswith('__') and not node.attr.endswith('__'):
                raise ValueError(f"Attribute access '{node.attr}' is forbidden")
        self.generic_visit(node)

# ------------------------------------------------------------------------------
def process_python_code(code_str: str):
    """
    Execute a user provided Python code snippet in a restricted environment.

    Parameters
    ----------
    code_str : str
        The Python source to execute.

    Returns
    -------
    str | None
        Captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    # 1. Syntax check and forbid dangerous constructs
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    ForbiddenNodeVisitor().visit(parsed)

    # 2. Compile the code
    compiled = compile(parsed, filename='<user_code>', mode='exec')

    # 3. Prepare restricted globals/locals
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}
    sandbox_locals = {}

    # 4. Execute and capture stdout
    output_buf = StringIO()
    try:
        with redirect_stdout(output_buf):
            exec(compiled, sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error: {exc}") from exc

    result = output_buf.getvalue()
    return result if result else None
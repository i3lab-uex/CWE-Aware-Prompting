import ast
import builtins
import io
import sys
from types import ModuleType

# ------------------------------------------------------------------------------
# 1.  Disallowed AST node / call patterns
# ------------------------------------------------------------------------------

DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Global,          # disallow global modification
    ast.Nonlocal,
)

DISALLOWED_FUNCTIONS = {
    'eval',
    'exec',
    'open',
    '__import__',
    'compile',
    'input',             # avoid interactive input
}

# ------------------------------------------------------------------------------
# 2.  AST visitor that enforces the restrictions
# ------------------------------------------------------------------------------

class _SafeCodeChecker(ast.NodeVisitor):
    """
    Walks the AST of a code string and raises ValueError if it contains
    any disallowed constructs.
    """
    def __init__(self, code_str: str):
        self.code_str = code_str

    # ---- Node checks --------------------------------------------------------

    def generic_visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to certain builtins
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system()
            func_name = node.func.attr

        if func_name in DISALLOWED_FUNCTIONS:
            raise ValueError(f"Disallowed function call: {func_name}")

        # disallow attribute access on builtins like __import__
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'builtins':
                raise ValueError(f"Disallowed builtins attribute access: {node.func.attr}")

        self.generic_visit(node)

# ------------------------------------------------------------------------------
# 3.  Safe execution environment
# ------------------------------------------------------------------------------

def evaluate_code_string(code_string: str):
    """
    Execute *code_string* in a sandboxed environment that forbids imports,
    file I/O, and dangerous builtins.  If the code prints something to
    stdout, that output is returned as a string; otherwise None is returned.
    
    Parameters
    ----------
    code_string : str
        Python source to execute.

    Returns
    -------
    str | None
        Captured stdout, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code uses any disallowed operation.
    """
    # 1.  Verify safety via AST
    try:
        parsed = ast.parse(code_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    _SafeCodeChecker(code_string).visit(parsed)

    # 2.  Prepare a restricted global namespace
    safe_builtins = {k: v for k, v in builtins.__dict__.items()
                     if k not in ('__import__', 'open', 'eval', 'exec',
                                  'compile', 'input')}

    # Provide a minimal set of useful builtins
    safe_builtins.update({
        'abs': abs,
        'len': len,
        'range': range,
        'print': print,
    })

    globals_dict = {'__builtins__': safe_builtins}
    locals_dict: dict = {}

    # 3.  Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename="<string>", mode="exec"),
             globals_dict,
             locals_dict)
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
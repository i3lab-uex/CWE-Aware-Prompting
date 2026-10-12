import ast
import io
import sys
from types import FunctionType

# --------------------------------------------------------------------------- #
# 1.  Whitelist of safe built‑ins
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
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

# --------------------------------------------------------------------------- #
# 2.  AST visitor that ensures the code only uses allowed constructs
# --------------------------------------------------------------------------- #
class _SafetyVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if a disallowed node is found.
    """

    # Nodes that are inherently unsafe
    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,            # Python 2 only, but keep for completeness
        ast.Call,            # we will inspect calls separately
    )

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow calls to forbidden built‑ins or functions that may
        # perform I/O or side effects.
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # If the function is not in SAFE_BUILTINS, reject it.
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Call to unsafe function '{func_name}'")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system() or subprocess.call()
            raise ValueError(f"Attribute calls are disallowed: {ast.dump(node.func)}")
        else:
            raise ValueError(f"Unsupported call type: {ast.dump(node.func)}")

        # Recursively visit arguments
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow attribute access on any object (e.g., os.path)
        raise ValueError(f"Attribute access is disallowed: {ast.dump(node)}")

    def visit_Subscript(self, node: ast.Subscript):
        # Disallow subscript on arbitrary objects (e.g., open(...)[0])
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Import(self, node: ast.Import):
        raise ValueError("Imports are disallowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Imports are disallowed")

    def visit_Global(self, node: ast.Global):
        raise ValueError("Global declarations are disallowed")

    def visit_Nonlocal(self, node: ast.Nonlocal):
        raise ValueError("Nonlocal declarations are disallowed")

# --------------------------------------------------------------------------- #
# 3.  The main function
# --------------------------------------------------------------------------- #
def process_code_input(code_input: str):
    """
    Execute a small Python code snippet in a restricted environment.

    Parameters
    ----------
    code_input : str
        The Python source to run. It may contain multiple statements.

    Returns
    -------
    None or str
        If the code prints something, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or attempts unsafe calls.
    """
    # 1. Parse and validate the AST
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    _SafetyVisitor().visit(parsed)

    # 2. Prepare a sandboxed execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"),
             exec_globals,
             exec_locals)
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
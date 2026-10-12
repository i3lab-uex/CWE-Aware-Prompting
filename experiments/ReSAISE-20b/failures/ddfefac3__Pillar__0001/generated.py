import ast
import io
import sys
from types import SimpleNamespace

# ----------------------------------------------------------------------
# Helper: list of allowed built‑in names
_ALLOWED_BUILTINS = {
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
    'set': set,
    'str': str,
    'tuple': tuple,
    'sum': sum,
}

# ----------------------------------------------------------------------
class _ForbiddenNodeVisitor(ast.NodeVisitor):
    """Detect disallowed AST nodes."""
    def __init__(self):
        self.forbidden = []

    def visit_Import(self, node):
        self.forbidden.append((node.lineno, "import statements are forbidden"))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.forbidden.append((node.lineno, "from…import statements are forbidden"))
        self.generic_visit(node)

    def visit_Call(self, node):
        # disallow calls to dangerous built‑ins
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in {'open', 'eval', 'exec', '__import__'}:
                self.forbidden.append((node.lineno, f"call to '{name}' is forbidden"))
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # disallow accessing __import__ via attributes
        if isinstance(node.attr, str) and node.attr == "__import__":
            self.forbidden.append((node.lineno, "access to '__import__' is forbidden"))
        self.generic_visit(node)

    def visit_Global(self, node):
        # disallow global declarations
        self.forbidden.append((node.lineno, "global declaration is forbidden"))
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        # disallow nonlocal declarations
        self.forbidden.append((node.lineno, "nonlocal declaration is forbidden"))
        self.generic_visit(node)

# ----------------------------------------------------------------------
def process_python_code(code_str: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    code_str : str
        The Python source to execute.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden constructs or fails to parse.
    """
    # 1. Parse and validate syntax
    try:
        tree = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # 2. Inspect for forbidden nodes
    visitor = _ForbiddenNodeVisitor()
    visitor.visit(tree)
    if visitor.forbidden:
        msgs = "; ".join(f"line {ln}: {msg}" for ln, msg in visitor.forbidden)
        raise ValueError(f"Forbidden code detected: {msgs}")

    # 3. Prepare a safe globals dict
    safe_globals = {'__builtins__': _ALLOWED_BUILTINS}
    # 4. Prepare a locals dict to capture definitions
    safe_locals = {}

    # 5. Execute the code, capturing stdout if needed
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out
    try:
        # If the code consists of a single expression, evaluate it and return its value
        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
            result = eval(compile(ast.Expression(tree.body[0].value), '<string>', 'eval'),
                          safe_globals, safe_locals)
        else:
            exec(compile(tree, '<string>', 'exec'), safe_globals, safe_locals)
            result = None
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    return result
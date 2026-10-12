import ast
import builtins
import io
import sys
from types import ModuleType, FunctionType

# --------------------------------------------------------------------------- #
# Safe execution environment
# --------------------------------------------------------------------------- #

class ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Detects disallowed AST nodes in the user snippet.
    """

    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,                     # exec() statement (Python 2)
        ast.Call,                    # disallowed function calls are checked in visit_Call
    )

    def __init__(self):
        self.found_forbidden = False

    def generic_visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            self.found_forbidden = True
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to dangerous builtins or functions
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in {"eval", "exec", "__import__", "open"}:
                self.found_forbidden = True
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system(...)
            if isinstance(node.func.value, ast.Name) and node.func.value.id in {"os", "sys"}:
                self.found_forbidden = True
        super().visit_Call(node)


def _build_safe_builtins():
    """
    Construct a restricted dictionary of built-in functions that are safe for execution.
    """
    allowed_names = {
        "abs", "all", "any", "ascii", "bin", "bool",
        "chr", "complex", "dict", "divmod", "enumerate",
        "filter", "float", "format", "frozenset", "hash",
        "hex", "int", "isinstance", "issubclass", "iter",
        "len", "list", "map", "max", "min", "next", "object",
        "ord", "pow", "range", "repr", "reversed", "round",
        "set", "slice", "sorted", "str", "sum", "tuple",
        "zip"
    }
    safe_builtins = {name: getattr(builtins, name) for name in allowed_names}
    return safe_builtins


SAFE_BUILTINS = _build_safe_builtins()


def execute_python_code(snippet_code: str):
    """
    Execute a user-provided Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet_code : str
        The Python code to execute. May contain multiple statements.

    Returns
    -------
    Any
        The output captured from the snippet (e.g., via print()) or None if nothing was printed.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    # 1. Parse and validate the AST
    try:
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    visitor = ForbiddenNodeVisitor()
    visitor.visit(parsed)
    if visitor.found_forbidden:
        raise ValueError("Snippet contains forbidden operations (imports, eval, exec, os/system calls).")

    # 2. Prepare a sandboxed globals dict
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 3. Capture stdout
    original_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None
    finally:
        sys.stdout = original_stdout

    output = fake_out.getvalue()
    return output if output else None
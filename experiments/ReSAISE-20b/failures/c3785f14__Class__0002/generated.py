import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# List of disallowed AST node types and function names
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
)

DISALLOWED_NAMES = {
    "eval",
    "exec",
    "open",
    "__import__",
    "input",
    # functions that could access the file system or OS
    "os.system",
    "subprocess",
    "shutil",
}

# A minimal set of safe built‑ins
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

class _SafetyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        self.errors.append(f"Disallowed import statement at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.errors.append(f"Disallowed import-from statement at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for calls to disallowed names
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_NAMES:
            self.errors.append(f"Disallowed function call '{node.func.id}' at line {node.lineno}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system(...)
            full_name = self._get_full_attr(node.func)
            if full_name in DISALLOWED_NAMES:
                self.errors.append(f"Disallowed function call '{full_name}' at line {node.lineno}")
        self.generic_visit(node)

    def _get_full_attr(self, node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts))

    def generic_visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            self.errors.append(f"Disallowed node {type(node).__name__} at line {getattr(node, 'lineno', '?')}")
        super().generic_visit(node)

def evaluate_code_string(code_string: str):
    """
    Execute a Python code snippet in a sandboxed environment.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    str or None
        If the executed code writes to stdout, the captured output is returned.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs.
    """
    # Parse and validate syntax
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    visitor = _SafetyVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("Disallowed code detected:\n" + "\n".join(visitor.errors))

    # Prepare restricted globals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}

    # Capture output
    stdout_buffer = StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(tree, filename="<string>", mode="exec"), sandbox_globals)
    except Exception as exc:
        # Re‑raise exceptions from user code without exposing internal details
        raise RuntimeError(f"Execution error: {exc}") from exc

    output = stdout_buffer.getvalue()
    return output if output else None
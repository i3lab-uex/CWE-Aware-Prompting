import ast
import io
import sys
from types import SimpleNamespace

# List of built‑in names that are considered safe.
SAFE_BUILTINS = {
    "True", "False", "None",
    "len", "range", "min", "max", "sum",
    "abs", "round", "pow",
}

# Names that are explicitly forbidden (even if they appear in SAFE_BUILTINS)
FORBIDDEN_NAMES = {"open", "exec", "eval", "__import__", "compile"}

# Node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,           # function calls are checked separately
    ast.Attribute,      # attribute access (e.g., os.system)
    ast.Subscript,      # subscript of objects
    ast.Lambda,
    ast.Yield,
    ast.YieldFrom,
    ast.Await,
    ast.AsyncFunctionDef,
    ast.FunctionDef,
    ast.ClassDef,
)

class _SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, UNSAFE_NODES):
            self.errors.append(f"Disallowed construct: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # disallow calls to forbidden names
        func = node.func
        if isinstance(func, ast.Name) and func.id in FORBIDDEN_NAMES:
            self.errors.append(f"Disallowed function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            self.errors.append("Disallowed attribute call")
        super().visit_Call(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in SAFE_BUILTINS:
            self.errors.append(f"Disallowed name: {node.id}")
        super().visit_Name(node)

def _is_safe(snippet):
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}") from None

    visitor = _SafeVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError(f"Forbidden operations detected: {', '.join(visitor.errors)}")

    return tree

def run_python_snippet(snippet_string: str):
    """
    Execute a user provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_string : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    tree = _is_safe(snippet_string)

    # Prepare a minimal global namespace
    safe_globals = {name: __builtins__[name] for name in SAFE_BUILTINS if name in __builtins__}
    safe_globals["__builtins__"] = safe_globals

    # Capture stdout
    old_stdout = sys.stdout
    out_capture = io.StringIO()
    sys.stdout = out_capture

    try:
        # If the snippet is a single expression, evaluate it
        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
            expr = tree.body[0].value
            value = eval(compile(ast.Expression(expr), filename="<snippet>", mode="eval"),
                         safe_globals, {})
            return value if value is not None else None
        # Otherwise execute the snippet
        exec(compile(tree, filename="<snippet>", mode="exec"),
             safe_globals, {})
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None
    finally:
        sys.stdout = old_stdout

    # Return any printed output if needed (optional)
    out_text = out_capture.getvalue()
    return None

# Example usage:
if __name__ == "__main__":
    code = "x = 2 + 3\nprint('Result:', x)"
    print("Output:", run_python_snippet(code))
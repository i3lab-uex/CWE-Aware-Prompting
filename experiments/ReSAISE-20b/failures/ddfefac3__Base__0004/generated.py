import ast
import sys
import io
from types import ModuleType

class _SafeVisitor(ast.NodeVisitor):
    """
    AST visitor that forbids potentially dangerous nodes and calls.
    """

    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Global,
        ast.Nonlocal,
        ast.Lambda,
    )

    FORBIDDEN_CALLS = {
        "eval",
        "exec",
        "compile",
        "__import__",
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow calls to dangerous built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_CALLS:
            raise ValueError(f"Forbidden call to built‑in: {node.func.id}")
        # Disallow attribute calls like os.system
        if isinstance(node.func, ast.Attribute):
            raise ValueError(f"Forbidden attribute call: {ast.dump(node.func)}")
        self.generic_visit(node)


def _is_safe(code_str: str) -> None:
    """
    Validate that the code does not contain disallowed constructs.
    Raises ValueError if forbidden content is detected.
    """
    try:
        tree = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    visitor = _SafeVisitor()
    visitor.visit(tree)


def process_python_code(code_str: str):
    """
    Execute a user supplied Python snippet in a restricted environment.

    Parameters
    ----------
    code_str : str
        The user provided Python source code to be executed.

    Returns
    -------
    Any
        If the snippet produces a value that can be captured as the last
        expression (e.g. ``print`` statements are not captured), this value is
        returned; otherwise ``None``.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or calls, or is otherwise
        syntactically invalid.
    """
    # 1. Validate the code
    _is_safe(code_str)

    # 2. Prepare a restricted execution environment.
    safe_builtins = {
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
        "str": str,
        "sum": sum,
        "tuple": tuple,
        # add more safe builtins as needed
    }

    exec_globals = {"__builtins__": safe_builtins}
    exec_locals = {}

    # 3. Capture stdout temporarily
    old_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(code_str, exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # 4. Return the captured output if any, otherwise None
    out = captured_output.getvalue()
    return out if out else None

# Example usage (uncomment to test):
# print(process_python_code("print('Hello, world!')"))
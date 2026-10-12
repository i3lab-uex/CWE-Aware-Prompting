import ast
import builtins
import io
import sys
from types import ModuleType

# --------------------------------------------------------------------------- #
# Helper: Detect prohibited AST nodes -------------------------------------- #
# --------------------------------------------------------------------------- #

class RestrictedVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError on any disallowed constructs.
    """

    # Disallowed node types
    _bad_nodes = (
        ast.Import,          # import statements
        ast.ImportFrom,      # from ... import ...
        ast.Call,            # function calls are inspected separately
        ast.Exec,            # exec() in Python 2 (never present in Py3)
    )

    def __init__(self):
        super().__init__()
        self._prohibited_calls = {
            "open",
            "eval",
            "exec",
            "__import__",
            "compile",
        }

    def generic_visit(self, node):
        if isinstance(node, self._bad_nodes):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow certain built-in calls
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self._prohibited_calls:
                raise ValueError(f"Disallowed function call: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system()
            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id in {"os", "subprocess"}
            ):
                raise ValueError(f"Disallowed call to {node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
# Safe builtins whitelist ----------------------------------------------- #
# --------------------------------------------------------------------------- #

SAFE_BUILTINS = {
    # Basic types and functions
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "bytes": bytes,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "divmod": divmod,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "repr": repr,
    "round": round,
    "set": set,
    "slice": slice,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    # I/O
    "print": print,
}

# --------------------------------------------------------------------------- #
# Main function ------------------------------------------------------------ #
# --------------------------------------------------------------------------- #

def restricted_run_code(run_code: str):
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    run_code : str
        The Python source code to execute.

    Returns
    -------
    str | None
        Captured stdout output if the script writes to it, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # Parse and validate the AST
    try:
        tree = ast.parse(run_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Inspect the AST for prohibited constructs
    visitor = RestrictedVisitor()
    visitor.visit(tree)

    # Prepare restricted globals and locals
    safe_globals: dict = {"__builtins__": SAFE_BUILTINS}
    local_vars: dict = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Compile and execute
        code_obj = compile(tree, filename="<restricted>", mode="exec")
        exec(code_obj, safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        # Restore stdout
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
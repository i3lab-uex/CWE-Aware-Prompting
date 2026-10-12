import ast
import builtins
import io
import sys
from types import ModuleType

# --------------------------------------------------------------------------- #
# Helper: List of safe built‑ins that can be exposed to user code
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
    # Basic types & constructors
    "True": True,
    "False": False,
    "None": None,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,

    # Built‑in functions
    "len": len,
    "range": range,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,

    # Useful modules
    "math": __import__("math"),
}

# --------------------------------------------------------------------------- #
# AST visitor that rejects unsafe constructs
# --------------------------------------------------------------------------- #
class SafetyVisitor(ast.NodeVisitor):
    # Disallowed node types
    _DISALLOWED = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # calls are filtered by function name
        ast.Exec,          # exec is removed in Python 3
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
        ast.FunctionDef,   # allow but restrict body
        ast.Lambda,
    )

    # Function names that are disallowed when called
    _DISALLOWED_FUNCS = {
        "open",
        "__import__",
        "eval",
        "exec",
        "compile",
    }

    def visit(self, node):
        if isinstance(node, self._DISALLOWED):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Check the function being called
        if isinstance(node.func, ast.Name) and node.func.id in self._DISALLOWED_FUNCS:
            raise ValueError(f"Disallowed function call: {node.func.id}")
        # Also reject calls via attribute access (e.g., os.system)
        if isinstance(node.func, ast.Attribute):
            raise ValueError(f"Disallowed attribute call: {ast.dump(node.func)}")
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
# Main execution function
# --------------------------------------------------------------------------- #
def execute_python_code(snippet_code: str):
    """
    Execute a Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_code : str
        User supplied Python code to run.

    Returns
    -------
    Any
        The value returned by the snippet if it produces a single expression,
        otherwise the captured stdout as string.  If there is no output, returns
        None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or runtime errors.
    """
    if not isinstance(snippet_code, str):
        raise ValueError("snippet_code must be a string")

    # 1. Parse and validate the code
    try:
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Run safety checks
    SafetyVisitor().visit(parsed)

    # 2. Prepare a restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    out_capture = io.StringIO()
    sys.stdout = out_capture

    try:
        # If the snippet is a single expression, evaluate it
        if (
            len(parsed.body) == 1
            and isinstance(parsed.body[0], ast.Expr)
        ):
            result = eval(compile(parsed, "<string>", mode="eval"), safe_globals, safe_locals)
        else:
            exec(compile(parsed, "<string>", mode="exec"), safe_globals, safe_locals)
            result = None
    except Exception as exc:
        raise ValueError(f"Runtime error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 4. Return captured output or result
    output = out_capture.getvalue()
    if output:
        return output.rstrip("\n")
    return result
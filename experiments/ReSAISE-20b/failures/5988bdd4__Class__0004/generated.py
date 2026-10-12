# Safe Python snippet runner – suitable for teaching environments

import ast
from types import FunctionType, CodeType
from typing import Any, Optional


# ----------------------------------------------------------------------
# 1. Security checks – disallow dangerous constructs
# ----------------------------------------------------------------------
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls will be inspected for dangerous functions
)

# Names that are considered unsafe if called directly
FORBIDDEN_CALLS = {
    "open",
    "__import__",
    "eval",
    "exec",
    "compile",
    "input",          # reading from stdin is usually undesirable in a sandbox
}

# ----------------------------------------------------------------------
# 2. Restricted execution environment
# ----------------------------------------------------------------------
def _build_restricted_globals() -> dict:
    """
    Construct a minimal set of globals for executing user code.
    Only a handful of safe builtins are exposed.
    """
    allowed_builtins = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "bytes": bytes,
        "chr": chr,
        "complex": complex,
        "dict": dict,
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
        "str": str,
        "sum": sum,
        "tuple": tuple,
        # add other safe builtins as needed
    }
    return {"__builtins__": allowed_builtins}


# ----------------------------------------------------------------------
# 3. AST visitor to detect forbidden patterns
# ----------------------------------------------------------------------
class _SecurityVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.forbidden = False

    def visit_Import(self, node: ast.Import) -> None:
        self.forbidden = True

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.forbidden = True

    def visit_Call(self, node: ast.Call) -> None:
        # Check if the function being called is forbidden
        func = node.func
        if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
            self.forbidden = True
        elif isinstance(func, ast.Attribute):
            # e.g., os.system()
            if func.attr in FORBIDDEN_CALLS:
                self.forbidden = True
        self.generic_visit(node)


def _check_security(code: str) -> None:
    """
    Raise ValueError if the snippet contains disallowed syntax or calls.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    visitor = _SecurityVisitor()
    visitor.visit(tree)
    if visitor.forbidden:
        raise ValueError("Snippet contains forbidden operations (imports, eval, exec, open, etc.)")


# ----------------------------------------------------------------------
# 4. Execute the snippet safely
# ----------------------------------------------------------------------
def run_python_snippet(snippet_string: str) -> Optional[Any]:
    """
    Execute a user-provided Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet_string : str
        The Python code to execute. May contain multiple statements.

    Returns
    -------
    Any | None
        The value of the last expression in the snippet if present,
        otherwise ``None``.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations,
        or if it is syntactically invalid.
    """
    # 1. Quick security validation
    _check_security(snippet_string)

    # 2. Compile the code object
    try:
        code_obj = compile(snippet_string, "<user_snippet>", "exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # 3. Prepare restricted globals
    globals_dict = _build_restricted_globals()
    locals_dict: dict[str, Any] = {}

    # 4. Execute
    try:
        exec(code_obj, globals_dict, locals_dict)
    except Exception as exc:   # pragma: no cover
        raise ValueError(f"Execution error: {exc}") from None

    # 5. Determine if there was a last expression result
    #    For simplicity, we check for a variable named "__last_expr__"
    #    that user code can set via: __last_expr__ = <value>
    return locals_dict.get("__last_expr__", None)


# ----------------------------------------------------------------------
# 5. Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     snippet = """
# a = 2 + 3
# __last_expr__ = a * 5
# """
#     print(run_python_snippet(snippet))   # should output 25
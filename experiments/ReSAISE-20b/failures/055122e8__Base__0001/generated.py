import ast
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Safe execution helper
# --------------------------------------------------------------------------- #

SAFE_BUILTINS: Dict[str, Any] = {
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
    # add more if needed
}

# --------------------------------------------------------------------------- #
# AST validator
# --------------------------------------------------------------------------- #

class SafeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if a disallowed node is found.
    """

    def __init__(self):
        super().__init__()
        self._prohibited = {
            ast.Import,
            ast.ImportFrom,
            ast.Exec,               # Python 2 only; kept for completeness
            ast.Call,
            ast.Attribute,
        }

    def visit(self, node):
        if isinstance(node, tuple(self._prohibited)):
            self._handle_prohibited(node)
        super().visit(node)

    def _handle_prohibited(self, node):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValueError("Import statements are not allowed.")
        if isinstance(node, ast.Call):
            # disallow calls to eval/exec or any function whose name starts with '_' or is a
            # builtin that could be dangerous.  We also disallow calls via attribute access.
            func = node.func
            if isinstance(func, ast.Name):
                if func.id in ("eval", "exec", "__import__"):
                    raise ValueError(f"Calling '{func.id}' is prohibited.")
            elif isinstance(func, ast.Attribute):
                # e.g., os.system(...)
                raise ValueError("Attribute function calls are prohibited.")
        if isinstance(node, ast.Attribute):
            # disallow attribute access that could expose dangerous internals
            if isinstance(node.value, ast.Name) and node.value.id in ("os", "sys", "__import__"):
                raise ValueError(f"Access to '{node.value.id}' attributes is prohibited.")
        # Continue traversal
        self.generic_visit(node)


def _validate_code(code: str) -> None:
    """
    Validate that the code does not contain prohibited constructs.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    visitor = SafeVisitor()
    visitor.visit(tree)


# --------------------------------------------------------------------------- #
# Main execution function
# --------------------------------------------------------------------------- #

def execute_python_script(python_code: str) -> Any:
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    python_code : str
        The user supplied code to execute.

    Returns
    -------
    Any
        The value of the variable named `result` if it exists in the local scope,
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or is syntactically invalid.
    """
    # Validate syntax and prohibited constructs
    _validate_code(python_code)

    # Prepare a restricted globals dict
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    safe_locals: Dict[str, Any] = {}

    # Execute the code
    try:
        exec(python_code, safe_globals, safe_locals)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Execution error: {exc}") from exc

    # Return the value of a variable named 'result' if present
    return safe_locals.get("result", None)
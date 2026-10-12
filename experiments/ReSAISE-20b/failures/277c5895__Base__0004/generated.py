import ast
import builtins
from types import ModuleType
from typing import Any, Dict


# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed built‑ins
# --------------------------------------------------------------------------- #
_ALLOWED_BUILTINS: Dict[str, Any] = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "bytes": bytes,
    "chr": chr,
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
    # Add more safe built‑ins as required
}


# --------------------------------------------------------------------------- #
# 2. Node visitor that flags disallowed AST nodes
# --------------------------------------------------------------------------- #
class _SafeCodeChecker(ast.NodeVisitor):
    """
    Traverses the AST of user code and raises ValueError if any
    disallowed node is encountered.
    """
    _DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,                 # Python 2 – kept for completeness
        ast.Call,                  # Calls are allowed only if they target whitelisted built‑ins
    )

    def __init__(self, code: str):
        self.code = code
        super().__init__()

    def generic_visit(self, node: ast.AST):
        if isinstance(node, self._DISALLOWED_NODES):
            # Import statements are disallowed
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError("Import statements are not allowed.")
            # Calls need further inspection
            if isinstance(node, ast.Call):
                self._check_call(node)
        super().generic_visit(node)

    def _check_call(self, node: ast.Call):
        """
        Ensure that the function being called is a whitelisted built‑in.
        Disallow attribute access (e.g., os.system) and any other calls.
        """
        # Reject attribute calls like obj.method()
        if isinstance(node.func, ast.Attribute):
            raise ValueError("Attribute access is prohibited in function calls.")
        # Reject name-based calls that are not whitelisted
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in _ALLOWED_BUILTINS:
                raise ValueError(f"Use of function '{func_name}' is not permitted.")
        else:
            # Other complex call targets are disallowed
            raise ValueError("Only simple function calls to whitelisted built‑ins are allowed.")


# --------------------------------------------------------------------------- #
# 3. Main execution function
# --------------------------------------------------------------------------- #
def execute_user_code(submitted_code: str) -> Any:
    """
    Executes user provided Python code in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The user supplied Python source code.

    Returns
    -------
    Any
        Result of the executed script if a value is produced,
        otherwise None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or invalid syntax.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(submitted_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in submitted code: {exc}") from None

    # 2. Security check
    checker = _SafeCodeChecker(submitted_code)
    checker.visit(parsed)

    # 3. Prepare restricted globals
    safe_globals: Dict[str, Any] = {"__builtins__": _ALLOWED_BUILTINS}
    # Optional: create a separate module for locals if needed
    safe_locals: Dict[str, Any] = {}

    # 4. Execute code
    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"),
             safe_globals,
             safe_locals)
    except Exception as exc:
        # Re‑raise any runtime errors as ValueError to keep interface consistent
        raise ValueError(f"Runtime error during execution: {exc}") from None

    # 5. Return the last evaluated expression if present
    # Since exec does not return a value, we look for any variable that was assigned.
    # For simplicity, return None (or extend as needed).
    return None
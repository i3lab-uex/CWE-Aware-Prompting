import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO


# --------------------------------------------------------------------------- #
# 1. Whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    # Basic types & constructors
    "bool": bool,
    "int": int,
    "float": float,
    "str": str,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "range": range,
    # Simple utilities
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    # Safe I/O
    "print": print,
}

# --------------------------------------------------------------------------- #
# 2. AST visitor that rejects unsafe nodes
class _SafetyChecker(ast.NodeVisitor):
    """Detects disallowed syntax such as imports, exec, eval, etc."""
    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only; harmless but keep for completeness
        ast.Call,          # we will filter calls to unsafe builtins separately
        ast.Attribute,
    )

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden syntax: {type(node).__name__}")
        # Reject calls to unsafe built‑ins
        if isinstance(node, ast.Call):
            func = node.func
            # Handle direct name calls (e.g., eval(...))
            if isinstance(func, ast.Name):
                if func.id in {"eval", "exec", "__import__", "open"}:
                    raise ValueError(f"Forbidden function call: {func.id}")
            # Handle attribute calls (e.g., os.system)
            elif isinstance(func, ast.Attribute):
                raise ValueError(f"Forbidden attribute call: {ast.dump(node)}")
        super().visit(node)

# --------------------------------------------------------------------------- #
def evaluate_user_input(user_code: str):
    """
    Execute `user_code` in a restricted environment.

    Parameters
    ----------
    user_code : str
        The Python script submitted by the user.

    Returns
    -------
    str or None
        Captured stdout if the script prints anything; otherwise `None`.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or invalid syntax.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # 2. Safety check
    checker = _SafetyChecker()
    try:
        checker.visit(parsed)
    except ValueError as exc:
        raise ValueError(f"User code rejected: {exc}") from None

    # 3. Prepare restricted globals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Allow local variable definitions within the script
    safe_locals = {}

    # 4. Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 safe_globals,
                 safe_locals)
    except Exception as exc:
        # Runtime errors are not forbidden; re‑raise as ValueError
        raise ValueError(f"Runtime error during execution: {exc}") from None

    # 5. Return captured output if any
    result = output_buffer.getvalue()
    return result or None
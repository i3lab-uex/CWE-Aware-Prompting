import ast
import builtins
import io
import sys
from types import ModuleType
from typing import Any, Optional


# ----------------------------------------------------------------------
# Whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    # Functions
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
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
    # Constants
    "True": True,
    "False": False,
    "None": None,
}

# ----------------------------------------------------------------------
class ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any forbidden node is found.
    """

    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # we check the function name later
    )

    FORBIDDEN_NAMES = {
        "open",
        "exec",
        "eval",
        "compile",
        "input",
        "__import__",
        "os",
        "sys",
    }

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, self.FORBIDDEN_NODES):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError("Import statements are not allowed.")
            if isinstance(node, ast.Call):
                # disallow calls to dangerous builtins
                func = node.func
                if isinstance(func, ast.Name) and func.id in self.FORBIDDEN_NAMES:
                    raise ValueError(f"Call to forbidden function `{func.id}`.")
                if isinstance(func, ast.Attribute):
                    # e.g., os.system()
                    if (
                        isinstance(func.value, ast.Name)
                        and func.value.id in self.FORBIDDEN_NAMES
                    ):
                        raise ValueError(f"Call to forbidden attribute `{func.value.id}.{func.attr}`.")
        return super().visit(node)


# ----------------------------------------------------------------------
def execute_python_code(snippet_code: str) -> Optional[str]:
    """
    Execute a user supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet_code : str
        The code to execute.

    Returns
    -------
    Optional[str]
        Captured standard output if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """

    # 1. Syntax check & forbid dangerous nodes
    try:
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    ForbiddenNodeVisitor().visit(parsed)

    # 2. Prepare restricted globals
    safe_globals: dict = {"__builtins__": SAFE_BUILTINS}
    # Provide an empty module for locals (no globals can be created)
    safe_locals: dict = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    output_buffer = io.StringIO()
    try:
        sys.stdout = output_buffer
        exec(compile(parsed, filename="<sandbox>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = output_buffer.getvalue()
    return output if output else None
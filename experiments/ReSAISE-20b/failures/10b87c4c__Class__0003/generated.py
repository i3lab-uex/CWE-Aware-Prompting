import ast
import builtins
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# 1. Define a whitelist of safe built‑ins that students may use
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
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
    # Add more as needed
}

# --------------------------------------------------------------------------- #
# 2. AST visitor that flags disallowed constructs
class DisallowVisitor(ast.NodeVisitor):
    """Raise ValueError if forbidden syntax is detected."""
    def __init__(self, code: str) -> None:
        self.code = code

    # Disallowed imports
    def visit_Import(self, node: ast.Import) -> None:
        raise ValueError("Import statements are not allowed.")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        raise ValueError("Import statements are not allowed.")

    # Disallowed calls to dangerous built‑ins
    def visit_Call(self, node: ast.Call) -> None:
        # Disallow eval/exec/open and similar
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in {"eval", "exec", "open"}:
                raise ValueError(f"Use of '{func_name}' is prohibited.")
        self.generic_visit(node)

    # Disallow attribute access that could reach the real os module
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name):
            if node.value.id == "os":
                raise ValueError("Access to 'os' module is prohibited.")
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
def process_code_input(code_input: str) -> Optional[Any]:
    """
    Execute a small Python code snippet in a sandboxed environment.

    Parameters
    ----------
    code_input : str
        The Python source to run.  It may contain multiple statements.

    Returns
    -------
    Optional[Any]
        None if the snippet produced no value, otherwise the last evaluated expression.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs.
    """
    # 1. Basic syntax check & static analysis
    try:
        tree = ast.parse(code_input, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from exc

    DisallowVisitor(code_input).visit(tree)

    # 2. Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals: dict[str, Any] = {}

    # 3. Execute the code
    try:
        exec(compile(tree, filename="<sandbox>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as exc:
        # Re‑raise exceptions to the caller – they are user errors
        raise exc

    # 4. Return the last value if any (the same as eval)
    return sandbox_locals.get("_result")

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# if __name__ == "__main__":
#     code = """
# result = sum(range(5))
# _result = result
# """
#     print(process_code_input(code))  # Output: 10
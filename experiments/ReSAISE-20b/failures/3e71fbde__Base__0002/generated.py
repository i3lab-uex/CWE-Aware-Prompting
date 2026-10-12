import ast
from types import ModuleType, FunctionType

# --------------------------------------------------------------------------- #
# 1. Whitelist of safe built‑ins ------------------------------------------------
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes', 'chr', 'dict',
    'float', 'int', 'len', 'list', 'max', 'min', 'pow',
    'range', 'round', 'set', 'str', 'sum', 'tuple',
    'enumerate', 'zip', 'map', 'filter', 'print'
}

# --------------------------------------------------------------------------- #
# 2. Helper: check AST for disallowed nodes ---------------------------------
# --------------------------------------------------------------------------- #
class DisallowChecker(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if any disallowed node is found.
    """

    def __init__(self):
        self.disallowed = []

    def visit_Import(self, node: ast.Import):
        raise ValueError("Direct imports are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Direct imports are not allowed")

    def visit_Call(self, node: ast.Call):
        # Disallow calls to __import__ or eval/exec
        if isinstance(node.func, ast.Name):
            if node.func.id in {"__import__", "eval", "exec"}:
                raise ValueError(f"Call to {node.func.id} is disallowed")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow attribute access that could reach dangerous modules
        if isinstance(node.value, ast.Name) and node.value.id in {"os", "sys"}:
            raise ValueError(f"Access to attribute {node.attr} of {node.value.id} is disallowed")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        # Disallow names that are not in whitelist or built‑ins
        if node.id.startswith("__") and node.id.endswith("__"):
            raise ValueError(f"Access to special name {node.id} is disallowed")
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
# 3. Main function -------------------------------------------------------------
# --------------------------------------------------------------------------- #
def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    snippet : str
        The code to execute.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # 1. Parse into AST and check for unsafe constructs
    try:
        parsed = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python syntax: {e}") from None

    checker = DisallowChecker()
    try:
        checker.visit(parsed)
    except ValueError as e:
        raise

    # 2. Prepare a restricted execution environment
    safe_globals = {"__builtins__": {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}}
    # Allow a minimal set of built‑in functions that are needed by most snippets
    safe_globals.update({k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__})

    # 3. Execute the snippet
    try:
        exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals)
    except Exception as e:
        # Re‑raise with a generic message to avoid leaking internal details
        raise ValueError(f"Execution error: {e}") from None

    # 4. If the snippet defines a variable named 'result', return it
    if "result" in safe_globals:
        return safe_globals["result"]
    # Otherwise, no explicit result – return None
    return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Safe snippet
    print(run_code_snippet("result = 2 + 3"))   # Output: 5

    # Unsafe snippet – will raise ValueError
    try:
        run_code_snippet("import os\nos.system('echo unsafe')")
    except ValueError as exc:
        print(f"Caught error: {exc}")
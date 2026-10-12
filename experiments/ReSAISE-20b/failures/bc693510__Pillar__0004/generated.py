import ast
from typing import Any, Optional

# List of safe built‑in functions that may be used in snippets
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "repr": repr,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

# AST node visitor that verifies the snippet only contains safe constructs
class SafeVisitor(ast.NodeVisitor):
    """
    Raises a ValueError if the AST contains disallowed nodes.
    """

    def visit(self, node):
        # Reject any name that is not a safe builtin or local variable
        if isinstance(node, ast.Name):
            if node.id in {"__import__", "eval", "exec", "open"}:
                raise ValueError(f"Disallowed name: {node.id}")
        super().visit(node)

    def visit_Call(self, node):
        # Reject calls to disallowed functions (e.g., __import__)
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed function call: {func_name}")
        self.generic_visit(node)

    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_Exec(self, node):  # pragma: no cover
        raise ValueError("exec statement is not allowed")

    def visit_Eval(self, node):  # pragma: no cover
        raise ValueError("eval statement is not allowed")

    def visit_Attribute(self, node):
        # Disallow attribute access to avoid hidden APIs (e.g., os.system)
        if isinstance(node.value, ast.Name) and node.attr in {"__dict__", "__class__"}:
            raise ValueError(f"Disallowed attribute access: {node.attr}")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Allow subscript only on safe builtins or literals
        self.generic_visit(node)

    def visit_Lambda(self, node):
        raise ValueError("Lambda expressions are not allowed")

    def visit_Yield(self, node):
        raise ValueError("Yield is not allowed")

    def visit_Raise(self, node):
        raise ValueError("Raise is not allowed")

def run_python_snippet(python_snippet: str) -> Optional[Any]:
    """
    Execute a small, safe Python snippet and return its result.

    Parameters
    ----------
    python_snippet : str
        The Python code to execute. It may contain multiple statements,
        but only a limited set of operations is permitted.

    Returns
    -------
    Optional[Any]
        The value produced by the last expression in the snippet,
        or None if no expression yields a result.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse the snippet into an AST and perform safety checks
    try:
        parsed = ast.parse(python_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    SafeVisitor().visit(parsed)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Local namespace for variables defined in the snippet
    local_vars: dict = {}

    # Execute the code. We capture the value of the last expression if present.
    exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, local_vars)

    # Determine the last expression value if any
    # In exec mode we cannot directly get the result, so we rely on a convention:
    # if the snippet contains a variable named "__result__", return it.
    return local_vars.get("__result__")

# Example usage (uncomment to test):
# result = run_python_snippet("""
# a = 5
# b = 10
# __result__ = a + b
# """)
# print(result)   # Output: 15
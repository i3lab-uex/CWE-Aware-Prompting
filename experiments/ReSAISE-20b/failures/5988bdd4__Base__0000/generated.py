import ast
from types import FunctionType, ModuleType
from typing import Any

# --------------------------------------------------------------------------- #
# 1. Whitelist of allowed built‑ins
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "bytes": bytes,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "float": float,
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
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
}

# --------------------------------------------------------------------------- #
# 2. AST visitor that rejects dangerous nodes
# --------------------------------------------------------------------------- #
class SafeNodeVisitor(ast.NodeVisitor):
    """
    Walks an AST and raises ValueError if it contains disallowed nodes.
    """

    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only – kept for completeness
        ast.Call,         # We'll filter calls to forbidden names later
        ast.Attribute,
    )

    FORBIDDEN_CALLS = {
        "open",
        "eval",
        "exec",
        "__import__",
        "compile",
    }

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to forbidden functions
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_CALLS:
            raise ValueError(f"Forbidden function call: {node.func.id}")
        # disallow attribute calls like os.system(...)
        if isinstance(node.func, ast.Attribute):
            raise ValueError(f"Attribute calls are disallowed: {ast.dump(node.func)}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent accessing arbitrary attributes (e.g., __class__, __dict__)
        if isinstance(node.attr, str) and node.attr.startswith("__"):
            raise ValueError(f"Access to special attribute '{node.attr}' is disallowed")
        self.generic_visit(node)


# --------------------------------------------------------------------------- #
# 3. The main sandboxed execution function
# --------------------------------------------------------------------------- #
def run_python_snippet(snippet_string: str) -> Any:
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet_string : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression if present; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or attempts forbidden operations.
    """
    if not isinstance(snippet_string, str):
        raise ValueError("snippet_string must be a string")

    try:
        # Parse the code into an AST
        tree = ast.parse(snippet_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Validate the AST
    visitor = SafeNodeVisitor()
    try:
        visitor.visit(tree)
    except ValueError as exc:
        raise ValueError(f"Forbidden operation detected: {exc}") from None

    # Prepare the sandboxed environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals: dict[str, Any] = {}

    # Determine if the snippet is a single expression
    if (
        len(tree.body) == 1
        and isinstance(tree.body[0], ast.Expr)
        # The expression must be a simple value or call to safe functions
    ):
        expr_code = compile(tree, filename="<sandbox>", mode="eval")
        try:
            result = eval(expr_code, safe_globals, safe_locals)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Execution error: {exc}") from None
        return result

    # Otherwise compile as a module and execute
    code_obj = compile(tree, filename="<sandbox>", mode="exec")
    try:
        exec(code_obj, safe_globals, safe_locals)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Execution error: {exc}") from None

    # If the snippet defined a variable named 'result', return it
    if "result" in safe_locals:
        return safe_locals["result"]

    # Otherwise, no value to return
    return None


# --------------------------------------------------------------------------- #
# 4. Example usage (commented out)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     print(run_python_snippet("2 + 3"))          # 5
#     print(run_python_snippet("result = sum(range(10))"))  # None (but result in locals)
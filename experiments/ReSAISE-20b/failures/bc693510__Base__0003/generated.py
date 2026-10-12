import ast
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# 1.  Define a whitelist of safe built‑in functions
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
}

# --------------------------------------------------------------------------- #
# 2.  Helper to detect prohibited nodes
# --------------------------------------------------------------------------- #
class _SafeVisitor(ast.NodeVisitor):
    """
    Visitor that raises ValueError if it finds any node that is
    considered unsafe for the educational sandbox.
    """
    # Prohibited statement types
    _PROHIBITED_STMTS = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 legacy
    )
    # Prohibited expression types (function calls to dangerous names)
    _PROHIBITED_CALLS = {
        "open",
        "__import__",
        "eval",
        "exec",           # Python 3 built‑in exec() is a function
    }

    def generic_visit(self, node: ast.AST):
        if isinstance(node, self._PROHIBITED_STMTS):
            raise ValueError(f"Import statements are not allowed: {ast.dump(node)}")

        if isinstance(node, ast.Call):
            func = node.func
            # Only allow calls to whitelisted built‑ins or user defined names
            if isinstance(func, ast.Name):
                name = func.id
                if name in self._PROHIBITED_CALLS:
                    raise ValueError(f"Call to prohibited function '{name}'")
                if name not in SAFE_BUILTINS and name not in self._user_defined:
                    raise ValueError(f"Call to unknown function '{name}'")
            elif isinstance(func, ast.Attribute):
                # disallow any attribute access (e.g., os.system)
                raise ValueError(f"Attribute access is prohibited: {ast.dump(node)}")

        # Disallow lambda expressions to prevent hidden code
        if isinstance(node, ast.Lambda):
            raise ValueError("Lambda expressions are not allowed")

        # Disallow comprehensions that may produce side effects
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            raise ValueError("Comprehensions are not allowed")

        super().generic_visit(node)

    def __init__(self):
        self._user_defined = set()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._user_defined.add(node.name)
        # Allow function body to be checked
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._user_defined.add(node.name)
        super().generic_visit(node)


# --------------------------------------------------------------------------- #
# 3.  The main sandboxed execution function
# --------------------------------------------------------------------------- #
def run_python_snippet(python_snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet in a sandboxed environment.

    Parameters
    ----------
    python_snippet : str
        The user supplied Python code to execute.

    Returns
    -------
    Optional[Any]
        The value of the last expression in the snippet, if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or unsafe calls.
    """
    # 1. Parse the code into an AST
    try:
        parsed = ast.parse(python_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    # 2. Validate the AST for safety
    visitor = _SafeVisitor()
    visitor.visit(parsed)

    # 3. Prepare the execution environment
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals: dict[str, Any] = {}

    # 4. Execute the code
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error during execution: {exc}") from exc

    # 5. If the last node is an expression, evaluate and return its value
    if parsed.body:
        last_node = parsed.body[-1]
        if isinstance(last_node, ast.Expr):
            try:
                # Evaluate the expression in the same sandboxed environment
                result = eval(compile(last_node.value, filename="<sandbox>", mode="eval"),
                              sandbox_globals,
                              sandbox_locals)
                return result
            except Exception as exc:
                raise ValueError(f"Error evaluating expression: {exc}") from exc

    # No result to return
    return None


# --------------------------------------------------------------------------- #
# 4.  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     code = """
# x = 5
# y = 10
# x + y
# """
#     print(run_python_snippet(code))   # Output: 15
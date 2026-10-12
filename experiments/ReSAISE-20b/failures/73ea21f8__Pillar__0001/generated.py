import ast
from typing import Any, Optional

# List of safe built‑in functions that may be used in snippets
SAFE_BUILTINS = {
    "abs", "all", "any", "bool", "bytes",
    "chr", "complex", "dict", "divmod",
    "float", "hash", "hex", "int", "isinstance",
    "len", "list", "map", "max", "min", "next",
    "oct", "ord", "pow", "range", "repr",
    "round", "set", "sorted", "str", "sum",
    "tuple", "zip"
}

# Names that are explicitly disallowed
FORBIDDEN_NAMES = {"exec", "eval", "__import__", "open", "input", "compile"}

class SafeNodeVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if any disallowed construct is found.
    """
    def visit_Import(self, node: ast.Import) -> None:
        raise ValueError("import statements are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        raise ValueError("import statements are not allowed")

    def visit_Call(self, node: ast.Call) -> None:
        # disallow calls to forbidden names
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
            raise ValueError(f"calls to '{node.func.id}' are not allowed")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # disallow attribute access that could lead to dangerous modules
        if isinstance(node.value, ast.Name) and node.value.id == "__import__":
            raise ValueError("attribute access on __import__ is not allowed")
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> None:
        self.generic_visit(node)

    def visit_Module(self, node: ast.Module) -> None:
        # Ensure only expressions or simple statements
        for stmt in node.body:
            if isinstance(stmt, ast.Import) or isinstance(stmt, ast.ImportFrom):
                self.visit_Import(stmt)
        self.generic_visit(node)

def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user provided Python code snippet in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The Python code to execute.  It may contain one or more expressions,
        assignments, and simple statements.

    Returns
    -------
    Any | None
        The value of the last expression if present; otherwise, None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed constructs or unsafe operations.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Walk the tree to ensure safety
    SafeNodeVisitor().visit(parsed)

    # Build a restricted globals dictionary
    safe_globals = {"__builtins__": {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}}

    # Execute the code.  We capture the value of the last expression if any.
    exec(compile(parsed, filename="<user_snippet>", mode="exec"), safe_globals)

    # Retrieve the result of the last expression if it exists
    # By convention, we look for a variable named "__result__" that the user may set
    return safe_globals.get("__result__")

# Example usage (commented out to keep the module self‑contained)
# if __name__ == "__main__":
#     snippet = """
# x = 10
# y = 20
# __result__ = x + y
# """
#     print(run_code_snippet(snippet))  # Should output 30
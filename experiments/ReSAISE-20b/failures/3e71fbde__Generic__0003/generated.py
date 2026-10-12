import ast
import math
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Safe execution helper
# --------------------------------------------------------------------------- #

class _SafeNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any disallowed node is encountered.
    Allowed nodes:
        - Module, Expr, Call, Name, Constant, Tuple, List, Dict, Set
        - Attribute access only on allowed modules (currently 'math')
    Allowed function names:
        - builtins: len, abs, round
        - math functions: all from the math module
    """

    ALLOWED_BUILTINS = {"len", "abs", "round"}
    ALLOWED_MODULES = {"math"}

    def visit_Import(self, node: ast.Import):
        raise ValueError("Direct imports are disallowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Direct imports are disallowed")

    def visit_Call(self, node: ast.Call):
        # Allow calls to allowed functions or module attributes
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name not in self.ALLOWED_BUILTINS:
                raise ValueError(f"Calling function '{name}' is not allowed")
        elif isinstance(node.func, ast.Attribute):
            # Ensure the attribute belongs to an allowed module
            if not isinstance(node.func.value, ast.Name):
                raise ValueError("Only simple module function calls are allowed")
            mod_name = node.func.value.id
            if mod_name not in self.ALLOWED_MODULES:
                raise ValueError(f"Access to module '{mod_name}' is not allowed")
        else:
            raise ValueError("Only simple function calls are allowed")

        # Recursively visit arguments
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_Name(self, node: ast.Name):
        # Names are allowed only if they refer to builtins or module names
        if node.id not in self.ALLOWED_BUILTINS and node.id not in self.ALLOWED_MODULES:
            raise ValueError(f"Name '{node.id}' is not allowed")

    def generic_visit(self, node):
        # Reject any other node types (e.g., Import, Lambda, Exec)
        allowed = (
            ast.Module,
            ast.Expr,
            ast.Constant,
            ast.Tuple,
            ast.List,
            ast.Dict,
            ast.Set,
            ast.Call,
            ast.Name,
            ast.Attribute,
        )
        if not isinstance(node, allowed):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().generic_visit(node)


def _check_safety(snippet: str):
    """
    Parse the snippet and raise ValueError if any disallowed operation is found.
    """
    tree = ast.parse(snippet, mode="exec")
    visitor = _SafeNodeVisitor()
    visitor.visit(tree)


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def run_code_snippet(snippet: str) -> Any:
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python code to execute. It may be a single expression or multiple statements.

    Returns
    -------
    Any
        The value of the last evaluated expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # 1. Safety check
    _check_safety(snippet)

    # 2. Prepare safe globals
    safe_globals: Dict[str, Any] = {
        "__builtins__": {},
        "len": len,
        "abs": abs,
        "round": round,
        "math": math,
    }

    # 3. Determine if snippet is a single expression
    try:
        tree = ast.parse(snippet, mode="eval")
        # It's a single expression; evaluate it
        return eval(compile(tree, "<string>", mode="eval"), safe_globals)
    except SyntaxError:
        # Not a single expression; execute statements
        exec(compile(ast.parse(snippet, mode="exec"), "<string>", mode="exec"), safe_globals)
        return None

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # print(run_code_snippet("2 + 3 * 4"))          # -> 14
    # print(run_code_snippet("math.sqrt(16)"))     # -> 4.0
    # run_code_snippet("print('Hello')")           # Raises ValueError (print not allowed)
    pass
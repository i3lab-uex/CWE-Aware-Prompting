import ast
from types import FunctionType

# --------------------------------------------------------------------------- #
#  Safe execution environment
# --------------------------------------------------------------------------- #

# A minimal set of built‑ins that are safe for educational use.
SAFE_BUILTINS = {
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
    "tuple": tuple,
    "zip": zip,
}

# --------------------------------------------------------------------------- #
#  AST visitor to detect disallowed operations
# --------------------------------------------------------------------------- #

class DisallowVisitor(ast.NodeVisitor):
    """
    Walks an AST and raises ValueError if any disallowed node is encountered.
    """

    DISALLOWED_CALLS = {
        # Built‑in functions that could compromise security
        "eval", "exec",
        # Common modules/functions for shell access
        "open", "input",
    }

    DISALLOWED_ATTRS = {
        # Prevent attribute access that could reach dangerous modules
        ("os", "system"),
        ("subprocess", "run"),
    }

    def visit_Import(self, node: ast.Import):
        raise ValueError("Imports are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Imports are not allowed")

    def visit_Call(self, node: ast.Call):
        # Detect calls to disallowed built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in self.DISALLOWED_CALLS:
            raise ValueError(f"Call to disallowed function '{node.func.id}'")
        # Detect calls like os.system(...)
        if isinstance(node.func, ast.Attribute):
            attr_chain = self._get_attr_chain(node.func)
            if tuple(attr_chain) in self.DISALLOWED_ATTRS:
                raise ValueError(f"Call to disallowed attribute '{'.'.join(attr_chain)}'")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent attribute access that could reach dangerous modules
        if isinstance(node.value, ast.Name) and (node.value.id, node.attr) in self.DISALLOWED_ATTRS:
            raise ValueError(f"Access to disallowed attribute '{node.value.id}.{node.attr}'")
        self.generic_visit(node)

    def _get_attr_chain(self, node: ast.Attribute):
        """
        Recursively extract attribute chain (e.g., os.system -> ['os', 'system'])
        """
        parts = []
        while isinstance(node, ast.Attribute):
            parts.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.insert(0, node.id)
        return tuple(parts)

# --------------------------------------------------------------------------- #
#  Main evaluation function
# --------------------------------------------------------------------------- #

def evaluate_code_string(code_string: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_string : str
        The code to execute.  It may contain multiple statements, but must not
        perform disallowed operations such as imports or calling dangerous
        built‑ins.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the code attempts to perform a disallowed operation.
    """
    # 1. Parse the source into an AST
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    # 2. Validate the AST
    DisallowVisitor().visit(tree)

    # 3. Prepare restricted globals & locals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    local_vars = {}

    # 4. Execute the code
    exec(compile(tree, filename="<string>", mode="exec"), safe_globals, local_vars)

# --------------------------------------------------------------------------- #
#  Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     code = """
# x = 2
# y = 3
# print(x + y)
# """
#     evaluate_code_string(code)   # prints 5
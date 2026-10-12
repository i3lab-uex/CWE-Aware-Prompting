import ast
from typing import Any, Optional

# A set of disallowed built‑in names and module attributes
DISALLOWED_NAMES = {
    "eval",
    "exec",
    "open",
    "__import__",
    "input",
}
# Disallowed attribute chains (e.g. os.system, subprocess.Popen)
DISALLOWED_ATTRS = {
    ("os", "system"),
    ("subprocess", "Popen"),
    ("subprocess", "call"),
    ("subprocess", "run"),
}

# Whitelisted built‑ins that are generally safe
WHITELISTED_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "bytes",
    "chr",
    "complex",
    "dict",
    "float",
    "int",
    "len",
    "list",
    "max",
    "min",
    "pow",
    "range",
    "round",
    "str",
    "sum",
    "tuple",
}

class _SafeNodeVisitor(ast.NodeVisitor):
    """Walk the AST and raise ValueError on disallowed nodes."""
    def visit_Import(self, node: ast.Import) -> None:
        raise ValueError("import statements are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        raise ValueError("import statements are not allowed")

    def visit_Call(self, node: ast.Call) -> None:
        # Disallow calls to disallowed names
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_NAMES:
                raise ValueError(f"Use of '{func.id}' is prohibited")
        elif isinstance(func, ast.Attribute):
            # Resolve attribute chain
            attr_chain = self._get_attr_chain(func)
            if tuple(attr_chain) in DISALLOWED_ATTRS:
                raise ValueError(f"Use of '{'.'.join(attr_chain)}' is prohibited")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Prevent attribute access to dangerous objects (e.g., __class__ etc.)
        if node.attr.startswith("__") and not node.attr.endswith("__"):
            raise ValueError(f"Attribute access to '{node.attr}' is prohibited")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        # Disallow use of forbidden names unless they are whitelisted
        if node.id in DISALLOWED_NAMES and node.id not in WHITELISTED_BUILTINS:
            raise ValueError(f"Use of '{node.id}' is prohibited")
        self.generic_visit(node)

    def _get_attr_chain(self, node: ast.Attribute) -> list[str]:
        chain = []
        current = node
        while isinstance(current, ast.Attribute):
            chain.insert(0, current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            chain.insert(0, current.id)
        return chain

def execute_user_code(submitted_code: str) -> Optional[Any]:
    """
    Execute a user‑supplied Python script in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute. It must not contain import statements or any
        disallowed built‑ins.

    Returns
    -------
    Any | None
        The value of the variable `result` defined in the script, if any.
        Otherwise None.

    Raises
    ------
    ValueError
        If the code contains syntax errors or disallowed operations.
    """
    # Parse the code and perform static checks
    try:
        parsed = ast.parse(submitted_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in submitted code: {exc}") from exc

    # Run static analysis
    visitor = _SafeNodeVisitor()
    visitor.visit(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in WHITELISTED_BUILTINS}}
    safe_locals = {}

    # Execute the code
    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        # Re‑raise as ValueError to keep a consistent error type
        raise ValueError(f"Execution failed: {exc}") from exc

    # Return the value of 'result' if defined
    return safe_locals.get("result")
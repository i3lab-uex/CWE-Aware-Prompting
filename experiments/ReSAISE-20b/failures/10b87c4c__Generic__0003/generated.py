import ast
import io
import sys
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# Safety utilities
# --------------------------------------------------------------------------- #

class _DisallowedNodeVisitor(ast.NodeVisitor):
    """Detect disallowed AST nodes in user code."""
    # Map of node types to human‑readable names
    _DISALLOWED = {
        ast.Import: "import statement",
        ast.ImportFrom: "from ... import",
        ast.Call: "function call",          # specific calls handled below
        ast.Attribute: "attribute access",
        ast.Lambda: "lambda expression",
    }

    # Function names that are disallowed
    _DISALLOWED_CALLS = {
        "__import__",
        "eval",
        "exec",
        "open",
        "compile",
        "input",
    }

    def __init__(self):
        self.found = None

    def generic_visit(self, node):
        if self.found:
            return
        # Check for disallowed node types
        for typ, name in self._DISALLOWED.items():
            if isinstance(node, typ):
                self.found = name
                return
        # Special handling for Call nodes
        if isinstance(node, ast.Call):
            func = node.func
            # Allow built‑in functions that are safe (e.g., len, sum)
            if isinstance(func, ast.Name):
                if func.id in self._DISALLOWED_CALLS:
                    self.found = f"disallowed function call: {func.id}"
                    return
            elif isinstance(func, ast.Attribute):
                # Disallow any attribute access that might reach dangerous objects
                if isinstance(func.value, ast.Name) and func.value.id == "__builtins__":
                    self.found = f"disallowed attribute access: {func.attr}"
                    return
        # Recurse into child nodes
        super().generic_visit(node)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def process_code_input(code_input: str):
    """
    Execute a user supplied Python snippet in a restricted environment.

    Parameters
    ----------
    code_input : str
        The Python code to run.

    Returns
    -------
    None or str
        If the snippet writes anything to stdout, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or if execution fails.
    """
    # 1. Parse and inspect the AST for disallowed constructs
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    visitor = _DisallowedNodeVisitor()
    visitor.visit(parsed)
    if visitor.found:
        raise ValueError(f"Disallowed operation detected: {visitor.found}")

    # 2. Prepare a restricted execution environment
    safe_builtins = {
        name: getattr(__builtins__, name)
        for name in ("abs", "all", "any", "bool", "bytes",
                     "chr", "dict", "float", "int", "len",
                     "list", "max", "min", "pow", "range",
                     "round", "set", "str", "tuple")
    }

    # Remove dangerous builtins explicitly
    for bad in ("__import__", "eval", "exec", "open", "compile", "input"):
        safe_builtins.pop(bad, None)

    exec_globals = {"__builtins__": SimpleNamespace(**safe_builtins)}
    exec_locals = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer

    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"),
             exec_globals,
             exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None
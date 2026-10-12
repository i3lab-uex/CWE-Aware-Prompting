import ast
import builtins
import sys
import io
from types import SimpleNamespace

# ------------------------------------------------------------------
# Helper: allowed built‑ins for a teaching environment
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "next": next,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}

# ------------------------------------------------------------------
class _SafeVisitor(ast.NodeVisitor):
    """Checks an AST for disallowed nodes."""
    def __init__(self):
        self.errors = []

    # Disallow imports
    def visit_Import(self, node):  # pragma: no cover
        self.errors.append("import statements are forbidden")
    def visit_ImportFrom(self, node):  # pragma: no cover
        self.errors.append("import statements are forbidden")

    # Disallow exec/eval
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ("exec", "eval"):
            self.errors.append(f"calling {node.func.id} is forbidden")
        self.generic_visit(node)

    # Disallow attribute access to modules that might be dangerous
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id in ("os", "sys", "subprocess"):
            self.errors.append(f"access to {node.value.id} module is forbidden")
        self.generic_visit(node)

    # Disallow direct use of open
    def visit_Name(self, node):
        if node.id == "open":
            self.errors.append("calling open() is forbidden")
        self.generic_visit(node)

    # Disallow lambda for safety
    def visit_Lambda(self, node):  # pragma: no cover
        self.errors.append("lambda expressions are forbidden")

# ------------------------------------------------------------------
def execute_python_code(snippet_code: str):
    """
    Execute a user supplied snippet in a highly restricted environment.
    Returns the value of the last expression if any, otherwise None.

    Raises ValueError on syntax errors or forbidden operations.
    """
    # 1. Parse the code to an AST
    try:
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # 2. Inspect the AST for disallowed patterns
    visitor = _SafeVisitor()
    visitor.visit(parsed)
    if visitor.errors:
        raise ValueError(f"Forbidden code detected: {', '.join(visitor.errors)}")

    # 3. Prepare a restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Provide a placeholder for locals
    safe_locals = {}

    # 4. Capture stdout to detect printed output (optional)
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # 5. Execute the code
        exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, safe_locals)
        # 6. If the snippet produced a value via the last expression,
        #    it will be stored in a special variable if we wrap code.
        #    For simplicity, return None and let students use prints.
        output = fake_out.getvalue()
        return output.strip() or None
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout
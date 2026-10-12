import ast
import io
import sys
from types import ModuleType

# --------------------------------------------------------------------------- #
# 1. Disallowed AST node checks (CWE‑74 safe‑execution)                       #
# --------------------------------------------------------------------------- #

class DisallowedNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any disallowed operation is found.
    """

    DISALLOWED_CALLS = {
        "open",
        "exec",
        "eval",
        "compile",
        "input",
    }

    DISALLOWED_MODULES = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "shutil",
        "pathlib",
    }

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name.split('.')[0] in self.DISALLOWED_MODULES:
                raise ValueError(f"Import of module '{alias.name}' is disallowed.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module
        if module and module.split('.')[0] in self.DISALLOWED_MODULES:
            raise ValueError(f"Import from module '{module}' is disallowed.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Function name may be a Name or Attribute
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system -> disallow any attribute call on a disallowed module
            value = node.func.value
            if isinstance(value, ast.Name) and value.id in self.DISALLOWED_MODULES:
                raise ValueError(f"Call to '{value.id}.{node.func.attr}' is disallowed.")
            func_name = node.func.attr

        if func_name in self.DISALLOWED_CALLS:
            raise ValueError(f"Call to disallowed function '{func_name}' is not allowed.")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow attribute access on disallowed modules (e.g., os.path)
        if isinstance(node.value, ast.Name) and node.value.id in self.DISALLOWED_MODULES:
            raise ValueError(f"Attribute access on module '{node.value.id}' is disallowed.")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        # Prevent usage of certain built‑in names that could be dangerous
        if node.id in {"__import__", "globals", "locals"}:
            raise ValueError(f"Usage of built‑in '{node.id}' is disallowed.")
        self.generic_visit(node)


# --------------------------------------------------------------------------- #
# 2. Restricted execution environment                                         #
# --------------------------------------------------------------------------- #

def _safe_globals():
    """
    Return a dictionary of globals that provides a minimal, safe environment.
    Only built‑in functions that are deemed harmless are exposed.
    """
    allowed_builtins = {
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
        "print": print,
        "range": range,
        "round": round,
        "str": str,
        "sum": sum,
        "tuple": tuple,
    }
    return {"__builtins__": allowed_builtins}


# --------------------------------------------------------------------------- #
# 3. Main function                                                            #
# --------------------------------------------------------------------------- #

def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet : str
        The code to execute. May contain multiple statements.

    Returns
    -------
    None or str
        If the snippet prints nothing, returns None. Otherwise,
        returns the captured stdout as a string.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # 1. Parse the code and validate
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    visitor = DisallowedNodeVisitor()
    visitor.visit(tree)

    # 2. Prepare sandboxed globals
    safe_globals = _safe_globals()
    local_vars: dict = {}

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, local_vars)
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
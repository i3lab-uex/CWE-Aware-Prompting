import ast
from types import SimpleNamespace
from contextlib import redirect_stdout
from io import StringIO


# --------------------------------------------------------------------------- #
# 1.  Define the set of allowed built‑ins
# --------------------------------------------------------------------------- #
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
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
    "print": print,  # Note: printing goes to stdout captured by the caller
}

# --------------------------------------------------------------------------- #
# 2.  Prohibited node types / functions / modules
# --------------------------------------------------------------------------- #
PROHIBITED_NODES = {
    ast.Import,
    ast.ImportFrom,
}

# Names of functions that are disallowed when called
PROHIBITED_FUNC_NAMES = {
    "eval",
    "exec",
    "__import__",
}

# Module names that are disallowed when used as attributes
PROHIBITED_MODULES = {
    "os",
    "subprocess",
    "sys",
    "shutil",
    "pickle",
    "socket",
}

# --------------------------------------------------------------------------- #
# 3.  AST visitor to detect prohibited constructs
# --------------------------------------------------------------------------- #
class ProhibitedUsageVisitor(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def generic_visit(self, node):
        if self.found:
            return  # early exit
        super().generic_visit(node)

    def visit_Import(self, node):
        self.found = True

    def visit_ImportFrom(self, node):
        self.found = True

    def visit_Call(self, node):
        # disallow calls to banned functions
        func = node.func
        if isinstance(func, ast.Name) and func.id in PROHIBITED_FUNC_NAMES:
            self.found = True
        # disallow calls to modules via attribute access (e.g., os.system)
        elif isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Name) and func.value.id in PROHIBITED_MODULES:
                self.found = True
        super().visit_Call(node)

    def visit_Attribute(self, node):
        # disallow attribute access on banned modules (e.g., os.getenv)
        if isinstance(node.value, ast.Name) and node.value.id in PROHIBITED_MODULES:
            self.found = True
        super().visit_Attribute(node)


# --------------------------------------------------------------------------- #
# 4.  The safe_run_script function
# --------------------------------------------------------------------------- #
def safe_run_script(script_code: str):
    """
    Execute *script_code* safely.

    Returns:
        The value of the last expression if present, otherwise None.
    Raises:
        ValueError: If syntax is invalid or prohibited constructs are detected.
    """
    # 1. Parse the code to check syntax
    try:
        parsed = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from None

    # 2. Walk the AST to detect disallowed constructs
    visitor = ProhibitedUsageVisitor()
    visitor.visit(parsed)
    if visitor.found:
        raise ValueError("Script contains prohibited operations (imports, eval, exec, etc.)")

    # 3. Prepare the execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    local_vars = {}

    # 4. Execute the script
    stdout_capture = StringIO()
    try:
        with redirect_stdout(stdout_capture):
            exec(compile(parsed, filename="<safe_script>", mode="exec"), safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None

    # 5. If the last node is an expression, evaluate and return its value
    if parsed.body:
        last_node = parsed.body[-1]
        if isinstance(last_node, ast.Expr):
            try:
                return eval(compile(ast.Expression(body=last_node.value),
                                    filename="<safe_script>",
                                    mode="eval"),
                            safe_globals, local_vars)
    return None
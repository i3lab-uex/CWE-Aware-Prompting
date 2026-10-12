import ast
import builtins
import sys
import io
from types import ModuleType

# ----------------------------------------------------------------------
# 1. Define a whitelist of safe built‑in functions
# ----------------------------------------------------------------------
SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in [
        "abs", "all", "any", "bool", "chr", "dict", "float",
        "int", "len", "list", "max", "min", "pow", "range",
        "round", "str", "sum", "tuple", "zip",
    ]
}

# ----------------------------------------------------------------------
# 2. AST visitor that rejects disallowed syntax
# ----------------------------------------------------------------------
class DisallowVisitor(ast.NodeVisitor):
    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # calls are filtered more precisely below
        ast.Attribute,
    )

    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            self.errors.append(
                f"Disallowed construct: {type(node).__name__}"
            )
        super().generic_visit(node)

    def visit_Call(self, node):
        # disallow calls to built‑in functions that can compromise safety
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # allow only whitelisted built‑ins; everything else is blocked
            if func_name not in SAFE_BUILTINS:
                self.errors.append(
                    f"Disallowed function call: {func_name}"
                )
        elif isinstance(node.func, ast.Attribute):
            # any attribute access (e.g., os.system) is forbidden
            self.errors.append(
                f"Disallowed attribute call: {ast.dump(node.func)}"
            )
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # attribute access is generally unsafe (e.g., __dict__, __class__)
        self.errors.append(f"Disallowed attribute access: {ast.dump(node)}")
        self.generic_visit(node)


# ----------------------------------------------------------------------
# 3. The core function
# ----------------------------------------------------------------------
def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet : str
        The Python code to run.

    Returns
    -------
    str | None
        Captured standard output from the snippet or ``None`` if nothing was printed.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or attempts to use unsafe built‑ins.
    """
    # 3.1: Quick sanity check – empty or whitespace only
    if not snippet.strip():
        return None

    # 3.2: Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # 3.3: Inspect the AST for disallowed constructs
    visitor = DisallowVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("Disallowed code detected: " + "; ".join(visitor.errors))

    # 3.4: Prepare a restricted global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 3.5: Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compile(tree, filename="<snippet>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None
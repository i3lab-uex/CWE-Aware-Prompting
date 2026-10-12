import ast
import builtins
import io
import sys
from types import SimpleNamespace


# --------------------------------------------------------------------------- #
# 1. Define a whitelist of safe built‑ins that students are allowed to use.
# --------------------------------------------------------------------------- #
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
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    # useful helpers
    "print": print,
}

# --------------------------------------------------------------------------- #
# 2. AST visitor that rejects disallowed nodes.
# --------------------------------------------------------------------------- #
class SafeVisitor(ast.NodeVisitor):
    """
    Traverses the AST and raises ValueError if it finds a node that
    performs potentially dangerous operations.
    """
    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # disallow arbitrary function calls
        ast.Exec,          # Python 2
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
        ast.Try,           # allow try/except? no
    )

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden operation: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # allow calls only to whitelisted builtins
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_BUILTINS:
            # recursively check arguments
            super().visit(node)
        else:
            raise ValueError(f"Disallowed function call: {ast.unparse(node)}")


# --------------------------------------------------------------------------- #
# 3. Execute the snippet safely.
# --------------------------------------------------------------------------- #
def execute_python_code(snippet_code: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet_code : str
        The code to execute.

    Returns
    -------
    Any
        Value of the last expression in the snippet, or None if there is no
        result.

    Raises
    ------
    ValueError
        If the snippet contains forbidden syntax or operations, or if it fails
        to compile.
    """
    # 3.1 Parse and validate the code
    try:
        tree = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    SafeVisitor().visit(tree)

    # 3.2 Prepare restricted globals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 3.3 Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Compile the AST to a code object
        code_obj = compile(tree, filename="<sandbox>", mode="exec")
        exec(code_obj, sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 3.4 Return the value of the last expression if any
    result = sandbox_locals.get("_", None)
    return result


# --------------------------------------------------------------------------- #
# 4. Optional: convenience wrapper that sets '_' to the value of the last
#    expression (if any). This is used by the interpreter below.
# --------------------------------------------------------------------------- #
def _run_snippet(code: str):
    """
    Helper that mimics the interactive interpreter by storing the last
    expression in '_' in the local namespace.
    """
    tree = ast.parse(code, mode="exec")
    # Insert a final assignment of the last expression to '_'
    if tree.body:
        last = tree.body[-1]
        if isinstance(last, ast.Expr):
            assign = ast.Assign(
                targets=[ast.Name(id="_", ctx=ast.Store())],
                value=last.value,
            )
            tree.body[-1] = assign
    exec(compile(tree, filename="<sandbox>", mode="exec"),
         {"__builtins__": SAFE_BUILTINS}, {})
    return None  # the result is in the sandbox, not returned

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# >>> execute_python_code("a = 5\nb = a * 2\nprint(b)\n")
# 10
#
# >>> execute_python_code("open('file.txt', 'w')")   # raises ValueError
#
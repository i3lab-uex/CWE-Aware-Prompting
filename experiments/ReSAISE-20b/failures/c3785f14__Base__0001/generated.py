import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
# 1. Safety checks – forbidden AST nodes
# --------------------------------------------------------------------------- #

class ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Walks an AST and raises a ValueError if it encounters any node that
    would allow the code to perform disallowed operations.
    """
    # Nodes representing imports or dynamic execution
    forbidden_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # we will check calls to disallowed functions
    )

    def __init__(self):
        self._has_forbidden_call = False

    def visit(self, node):
        if isinstance(node, self.forbidden_nodes):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError("Import statements are not allowed.")
            elif isinstance(node, ast.Call):
                self._check_call(node)
        # Continue traversal
        super().visit(node)

    def _check_call(self, node):
        """
        Disallow calls to __import__, eval, exec, open, compile,
        globals(), locals() and any attribute access on builtins.
        """
        # Call targets can be Name or Attribute
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in {"__import__", "eval", "exec", "open",
                             "compile", "globals", "locals"}:
                raise ValueError(f"Call to disallowed function '{func_name}'.")
        elif isinstance(node.func, ast.Attribute):
            # e.g., builtins.open(...)
            if (isinstance(node.func.value, ast.Name) and
                node.func.value.id == "builtins"):
                raise ValueError(f"Call to disallowed built-in '{node.func.attr}'.")
        # Recursively check arguments for nested calls
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
# 2. Safe globals / builtins
# --------------------------------------------------------------------------- #

def _safe_globals():
    """
    Returns a dictionary of globals that can be used by the executed code.
    Only a minimal set of builtins is exposed to reduce risk.
    """
    allowed_builtins = {
        "print": print,
        "len": len,
        "range": range,
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "sum": sum,
        "min": min,
        "max": max,
    }
    return {"__builtins__": allowed_builtins}

# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #

def evaluate_code_string(code_string: str):
    """
    Executes a small Python code snippet in a sandboxed environment.

    Parameters
    ----------
    code_string : str
        The Python source code to execute.

    Returns
    -------
    None or str
        If the executed code prints nothing, returns None.
        Otherwise, returns a string containing all printed output.

    Raises
    ------
    ValueError
        If the code attempts to perform disallowed operations.
    SyntaxError
        If the source code cannot be parsed.
    """
    # 1. Parse and check for forbidden nodes
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as exc:
        raise SyntaxError(f"Syntax error in code: {exc}") from exc

    visitor = ForbiddenNodeVisitor()
    visitor.visit(tree)

    # 2. Prepare sandboxed environment
    globals_dict = _safe_globals()
    locals_dict = {}

    # 3. Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(tree, filename="<sandbox>", mode="exec"),
                 globals_dict,
                 locals_dict)
    except Exception as exc:
        # Re‑raise any exception that occurs during execution
        raise exc

    output = output_io.getvalue()
    return output if output else None
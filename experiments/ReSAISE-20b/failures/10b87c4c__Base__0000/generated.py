import ast
import builtins
import contextlib
import io
from types import ModuleType, FunctionType


# --------------------------------------------------------------------------- #
#   Safety checks for the code that will be executed
# --------------------------------------------------------------------------- #

class _DisallowedNodeVisitor(ast.NodeVisitor):
    """
    Visitor that raises ValueError if the code contains disallowed AST nodes
    or calls to dangerous built‑ins.
    """
    # Names of built‑ins that are considered unsafe
    _dangerous_builtins = {
        "eval", "exec", "compile",
        "open", "__import__", "input",
    }

    def visit_Import(self, node: ast.Import) -> None:
        raise ValueError("Use of 'import' statements is disallowed")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        raise ValueError("Use of 'from ... import' statements is disallowed")

    def visit_Call(self, node: ast.Call) -> None:
        # Detect calls to disallowed built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in self._dangerous_builtins:
            raise ValueError(f"Call to disallowed builtin '{node.func.id}'")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Prevent attribute access that could lead to unsafe operations
        if isinstance(node.value, ast.Name) and node.value.id == "__builtins__":
            raise ValueError("Access to '__builtins__' is disallowed")
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global) -> None:
        raise ValueError("Global statements are disallowed")

    def visit_Nonlocal(self, node: ast.Nonlocal) -> None:
        raise ValueError("Nonlocal statements are disallowed")


def _check_code_safety(code: str) -> None:
    """
    Parse the code into an AST and run the safety visitor.
    Raises ValueError if disallowed constructs are found.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in supplied code: {exc}") from exc

    _DisallowedNodeVisitor().visit(tree)


# --------------------------------------------------------------------------- #
#   Restricted execution environment
# --------------------------------------------------------------------------- #

def _restricted_globals() -> dict:
    """
    Build a dictionary of globals that is safe for execution.
    Only expose a minimal set of built‑ins required for basic operations.
    """
    safe_builtins = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "chr": chr,
        "divmod": divmod,
        "enumerate": enumerate,
        "filter": filter,
        "float": float,
        "int": int,
        "len": len,
        "list": list,
        "map": map,
        "max": max,
        "min": min,
        "pow": pow,
        "range": range,
        "repr": repr,
        "round": round,
        "sorted": sorted,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        "zip": zip,
    }
    return {"__builtins__": safe_builtins}


# --------------------------------------------------------------------------- #
#   Main public API
# --------------------------------------------------------------------------- #

def process_code_input(code_input: str) -> None | object:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The code to execute. It may contain multiple statements.

    Returns
    -------
    None or object
        If the code prints something, that output is returned as a string.
        Otherwise, if the last statement evaluates to a value (e.g. an expression),
        that value is returned.  If there is no output or result, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or syntax.
    """
    # 1. Basic safety check
    _check_code_safety(code_input)

    # 2. Prepare execution environment
    globals_dict = _restricted_globals()
    locals_dict: dict = {}

    # 3. Capture stdout
    stdout_capture = io.StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        # 4. Execute the code
        try:
            exec(code_input, globals_dict, locals_dict)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Execution error: {exc}") from exc

    # 5. Determine return value
    output = stdout_capture.getvalue()

    if output:
        return output.rstrip("\n")

    # If the last line was an expression, it will be in locals under a special key
    # but exec does not return it.  We therefore evaluate the code in eval mode if
    # it consists of a single expression.
    stripped = code_input.strip()
    try:
        last_expr = ast.parse(stripped, mode="eval")
    except SyntaxError:
        return None  # not a single expression
    try:
        result = eval(compile(last_expr, "<string>", "eval"),
                      globals_dict, locals_dict)
        return result
    except Exception:
        return None  # evaluation failed; nothing to return
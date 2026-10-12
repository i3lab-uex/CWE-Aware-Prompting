import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO


class ForbiddenCodeError(ValueError):
    """Raised when the snippet contains disallowed operations."""


def _is_forbidden(node: ast.AST) -> bool:
    """Return True if the node represents a forbidden construct."""
    # Disallow imports, exec/eval, open, os.system etc.
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return True
    if isinstance(node, ast.Exec):
        # Exec is only in Python 2 AST; keep for safety
        return True

    if isinstance(node, ast.Call):
        # Disallow calls to dangerous builtins
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in {"open", "exec", "eval", "compile", "input"}:
                return True
        if isinstance(func, ast.Attribute):
            # e.g., os.system(), subprocess.Popen()
            attr_chain = []
            cur = func
            while isinstance(cur, ast.Attribute):
                attr_chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                attr_chain.append(cur.id)
            # Reversed to get module.function order
            full_name = ".".join(reversed(attr_chain))
            if full_name in {
                "os.system",
                "subprocess.Popen",
                "subprocess.call",
                "subprocess.run",
            }:
                return True

    if isinstance(node, ast.Attribute):
        # Prevent attribute access that might expose hidden APIs
        return True

    if isinstance(node, ast.Lambda):
        # Lambdas are allowed but we still need to check inside
        pass

    return False


def _check_syntax_and_security(snippet: str) -> None:
    """
    Parse the snippet and raise ForbiddenCodeError if any forbidden
    construct is detected.
    """
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ForbiddenCodeError(f"Syntax error: {exc}") from exc

    for node in ast.walk(tree):
        if _is_forbidden(node):
            raise ForbiddenCodeError(f"Forbidden construct detected: {ast.dump(node)}")


def execute_python_code(snippet_code: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    Only safe builtins are exposed. The function returns any output
    produced by the snippet (captured from stdout) or None if there is no output.

    Raises:
        ValueError: If the snippet contains forbidden operations or invalid code.
    """
    _check_syntax_and_security(snippet_code)

    # Define a restricted set of builtins
    safe_builtins = {
        name: getattr(builtins, name)
        for name in (
            "abs",
            "all",
            "any",
            "bool",
            "chr",
            "dict",
            "enumerate",
            "filter",
            "float",
            "int",
            "len",
            "list",
            "map",
            "max",
            "min",
            "pow",
            "range",
            "reversed",
            "round",
            "sorted",
            "str",
            "sum",
            "tuple",
            "zip",
        )
    }

    # Prepare the globals dictionary for exec
    sandbox_globals = {"__builtins__": safe_builtins}

    # Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(snippet_code, sandbox_globals)
    except Exception as exc:
        raise ForbiddenCodeError(f"Execution error: {exc}") from exc

    output = output_buffer.getvalue()
    return output if output else None
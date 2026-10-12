import ast
import sys
import io
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# Safety utilities: disallow dangerous AST nodes and built‑ins
# --------------------------------------------------------------------------- #

DISALLOWED_NODES = (
    ast.Import,            # import statements
    ast.ImportFrom,
    ast.Exec,              # exec is removed in Python 3 but keep for safety
    ast.Call,              # calls to functions that we blacklist
)

# List of disallowed function names (built‑ins or others)
DISALLOWED_FUNCTIONS = {
    "open", "eval", "exec", "__import__", "compile",
    "input", "globals", "locals", "vars", "dir",
    # you can add more as needed
}

def _check_safety(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a disallowed construct
    is found.
    """
    for child in ast.walk(node):
        # Disallow certain node types entirely
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(child).__name__}")

        # Disallow calls to blacklisted functions
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names (e.g., open(...))
            if isinstance(func, ast.Name) and func.id in DISALLOWED_FUNCTIONS:
                raise ValueError(f"Disallowed function call: {func.id}")
            # Handle attribute access (e.g., os.system)
            if isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in DISALLOWED_FUNCTIONS:
                    raise ValueError(f"Disallowed function call: {attr_name}")

def _safe_builtins() -> dict:
    """
    Return a dictionary of safe built‑in functions. Only a minimal subset is
    provided to avoid accidental use of dangerous operations.
    """
    safe = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "chr": chr,
        "complex": complex,
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
        # add more safe built‑ins as needed
    }
    return safe

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def evaluate_code_string(code_string: str):
    """
    Execute a small Python snippet in a restricted environment.

    Parameters
    ----------
    code_string : str
        The Python source to run.

    Returns
    -------
    None or the value of the last expression, if present.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse and safety‑check the AST
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")

    _check_safety(tree)

    # Prepare a sandboxed environment
    sandbox_globals = {"__builtins__": _safe_builtins()}
    sandbox_locals = {}

    # Capture stdout/stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    fake_out = io.StringIO()
    sys.stdout = sys.stderr = fake_out

    try:
        # Execute the code
        exec(compile(tree, filename="<string>", mode="exec"), sandbox_globals, sandbox_locals)

        # If the last line is an expression, evaluate it
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            expr_code = compile(ast.Expression(body=tree.body[-1].value), filename="<string>", mode="eval")
            result = eval(expr_code, sandbox_globals, sandbox_locals)
        else:
            result = None

    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    finally:
        # Restore stdout/stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr

    # If there was printed output and no explicit result, return the output
    output = fake_out.getvalue()
    if output.strip():
        return output.strip()

    return result

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Should work
    print(evaluate_code_string("x = 5\nprint('Hello', x)\n"))
    # Should return the last expression
    print(evaluate_code_string("a = 10\nb = 20\n(a + b) * 2"))
    # Should raise ValueError
    try:
        evaluate_code_string("import os\nos.system('echo unsafe')")
    except ValueError as e:
        print(f"Caught error: {e}")
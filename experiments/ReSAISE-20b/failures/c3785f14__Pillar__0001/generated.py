import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO


class DisallowedNodeVisitor(ast.NodeVisitor):
    """
    Detects nodes that would allow potentially dangerous operations
    such as imports, attribute access to builtins, or calls to __import__.
    """

    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # we will filter calls further
        ast.Attribute,     # e.g., __builtins__.__import__
    )

    def __init__(self):
        self.found = False

    def generic_visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            # Specific handling for Call: reject __import__
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "__import__":
                    self.found = True
            else:
                self.found = True
        if not self.found:
            super().generic_visit(node)


def _is_safe(code_str: str) -> None:
    """
    Raise ValueError if the code string contains disallowed constructs.
    """
    try:
        tree = ast.parse(code_str, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    visitor = DisallowedNodeVisitor()
    visitor.visit(tree)

    if visitor.found:
        raise ValueError("Disallowed operation detected in code.")


def _create_safe_globals() -> dict:
    """
    Return a dictionary of globals that restricts access to unsafe objects.
    Only a minimal set of builtins is exposed.
    """
    safe_builtins = {
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
        "str": str,
        "sum": sum,
        "tuple": tuple,
    }
    return {"__builtins__": safe_builtins}


def evaluate_code_string(code_string: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_string : str
        The code to execute. It may contain multiple statements.

    Returns
    -------
    None or str
        If the code produces output via `print`, that output is returned as a string.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the code attempts to use disallowed operations (imports, __import__, etc.).
    """
    # 1. Verify safety
    _is_safe(code_string)

    # 2. Prepare restricted environment
    safe_globals = _create_safe_globals()
    safe_locals: dict = {}

    # 3. Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            # Compile and execute the code
            compiled = compile(code_string, "<string>", "exec")
            exec(compiled, safe_globals, safe_locals)
    except Exception as exc:
        # Re‑raise exceptions from user code without leaking internals
        raise type(exc)(str(exc)) from None

    # 4. Return captured output if any
    result = output_buffer.getvalue()
    return result or None


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(evaluate_code_string("print('Hello, world!')"))
#     print(evaluate_code_string("x = 5\nprint(x)"))
import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
# 1. Define a list of disallowed AST node types and function names
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,              # only for Python 2 compatibility
    ast.Global,
    ast.Nonlocal,
)

DISALLOWED_FUNCS = {
    "eval",
    "exec",
    "open",
    "input",
    "__import__",
}

# --------------------------------------------------------------------------- #
# 2. Visitor that checks the AST for disallowed constructs
class SecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            self.errors.append(f"Disallowed node: {type(node).__name__}")
        elif isinstance(node, ast.Call):
            # check function name if it's a simple identifier
            func = node.func
            if isinstance(func, ast.Name) and func.id in DISALLOWED_FUNCS:
                self.errors.append(f"Disallowed function call: {func.id}")
            # disallow attribute calls to dangerous builtins
            if isinstance(func, ast.Attribute):
                if (
                    isinstance(func.value, ast.Name)
                    and func.value.id == "builtins"
                    and func.attr in DISALLOWED_FUNCS
                ):
                    self.errors.append(f"Disallowed builtins.{func.attr} call")
        super().generic_visit(node)

# --------------------------------------------------------------------------- #
# 3. Safe builtins (you can extend this list as needed)
SAFE_BUILTINS = {
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
}

# --------------------------------------------------------------------------- #
def evaluate_code_string(code_string: str):
    """
    Execute a small Python snippet in a sandboxed environment.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    None or str
        `None` if the executed code produced no output.
        Otherwise, returns a string containing everything printed to stdout.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or tries to use unsafe functions.
    """
    # 1. Parse the code
    try:
        parsed = ast.parse(code_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # 2. Check for disallowed constructs
    checker = SecurityChecker()
    checker.visit(parsed)
    if checker.errors:
        raise ValueError(f"Disallowed code detected: {', '.join(checker.errors)}")

    # 3. Prepare restricted globals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 4. Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<sandbox>", mode="exec"),
                 sandbox_globals,
                 sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error: {exc}") from exc

    # 5. Return output if any
    output = output_buffer.getvalue()
    return output or None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(evaluate_code_string("print('Hello, world!')"))  # Should output the string
#     print(evaluate_code_string("x = 5\nprint(x)"))         # Should output '5'
#     print(evaluate_code_string("import os"))               # Raises ValueError
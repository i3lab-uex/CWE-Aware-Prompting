import ast
import builtins
import io
import sys
from types import ModuleType

# --------------------------------------------------------------------------- #
# 1. Safety checks
# --------------------------------------------------------------------------- #

class DisallowedNodeVisitor(ast.NodeVisitor):
    """AST visitor that raises ValueError on disallowed nodes."""
    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # we will filter specific calls below
    )

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to eval(), exec(), open(), __import__ and any
        # function from the builtins module that is potentially dangerous.
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in {"eval", "exec", "open", "__import__"}:
                raise ValueError(f"Disallowed call to built-in function '{name}'")
        self.generic_visit(node)


def _is_safe_code(code: str) -> None:
    """
    Raise ValueError if the code contains disallowed constructs.
    """
    tree = ast.parse(code, mode="exec")
    DisallowedNodeVisitor().visit(tree)


# --------------------------------------------------------------------------- #
# 2. Safe built‑in namespace
# --------------------------------------------------------------------------- #

def _safe_builtins() -> dict:
    """
    Return a dictionary of safe built‑in functions and types.
    Only a very small subset is exposed to the executed code.
    """
    allowed = [
        "abs", "all", "any", "bool", "chr", "dict", "float",
        "int", "len", "list", "max", "min", "pow", "range",
        "round", "str", "sum", "tuple", "zip"
    ]
    return {name: getattr(builtins, name) for name in allowed if hasattr(builtins, name)}


# --------------------------------------------------------------------------- #
# 3. Main evaluation function
# --------------------------------------------------------------------------- #

def evaluate_code_string(code_string: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the snippet prints anything, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Quick sanity check for empty string
    if not code_string.strip():
        return None

    # 2. Verify safety of the code
    _is_safe_code(code_string)

    # 3. Prepare restricted execution environment
    safe_globals = {"__builtins__": _safe_builtins()}
    safe_locals = {}

    # 4. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        # Compile and execute the code
        compiled = compile(code_string, "<string>", "exec")
        exec(compiled, safe_globals, safe_locals)
    finally:
        sys.stdout = old_stdout

    # 5. Return captured output if any
    output = fake_out.getvalue()
    return output or None


# --------------------------------------------------------------------------- #
# 4. Example usage (commented out)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(evaluate_code_string("print('Hello, world!')"))  # Should output the string
#     print(evaluate_code_string("x = 5\nprint(x)"))          # Should output '5'
#     print(evaluate_code_string("open('file.txt', 'w')"))   # Raises ValueError
import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# List of disallowed function names and node types
FORBIDDEN_FUNC_NAMES = {
    "open", "exec", "eval", "compile",
    "input",  # avoid interactive input
    "os", "subprocess", "sys", "__import__",
}
FORBIDDEN_NODE_TYPES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls are filtered by name
    ast.Attribute,     # prevent attribute access like os.system
)

class CodeSafetyChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, FORBIDDEN_NODE_TYPES):
            self.errors.append(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Check for disallowed function names
        func = node.func
        if isinstance(func, ast.Name) and func.id in FORBIDDEN_FUNC_NAMES:
            self.errors.append(f"Disallowed function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            # disallow calls to attributes of forbidden modules
            attr_chain = []
            cur = func
            while isinstance(cur, ast.Attribute):
                attr_chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                attr_chain.append(cur.id)
            full_name = ".".join(reversed(attr_chain))
            if any(part in FORBIDDEN_FUNC_NAMES for part in attr_chain):
                self.errors.append(f"Disallowed attribute call: {full_name}")
        super().generic_visit(node)

def process_code_input(code_input: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The code to execute.

    Returns
    -------
    None or str
        `None` if the snippet produced no output, otherwise a string containing the printed output.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse and check for safety violations
    try:
        tree = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    checker = CodeSafetyChecker()
    checker.visit(tree)

    if checker.errors:
        raise ValueError(f"Disallowed code detected: {', '.join(checker.errors)}")

    # Prepare a sandboxed global namespace
    sandbox_globals = {"__builtins__": {}}
    # Optionally expose safe built-ins
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
    }
    sandbox_globals["__builtins__"].update(allowed_builtins)

    # Capture stdout
    output_capture = StringIO()
    try:
        with redirect_stdout(output_capture):
            exec(compile(tree, filename="<string>", mode="exec"), sandbox_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    output = output_capture.getvalue()
    return output if output else None
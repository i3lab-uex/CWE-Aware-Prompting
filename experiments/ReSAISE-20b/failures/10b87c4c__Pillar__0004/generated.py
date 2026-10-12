import ast
import builtins
import sys
from contextlib import redirect_stdout
from io import StringIO

# Define a whitelist of safe built‑in functions/objects.
SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in [
        "abs",
        "all",
        "any",
        "bool",
        "chr",
        "dict",
        "float",
        "int",
        "len",
        "list",
        "max",
        "min",
        "pow",
        "print",
        "range",
        "round",
        "str",
        "sum",
    ]
}

# Disallowed AST node types or function names.
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,  # we will inspect the call separately
    ast.Lambda,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.ExceptHandler,
)

DISALLOWED_FUNC_NAMES = {
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "_import",
    "__import__",
    "execfile",  # Python 2
    "os.system",
    "subprocess",
    "shutil",
    "pickle",
}

def _check_disallowed(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if disallowed
    constructs are found.
    """
    for child in ast.walk(node):
        # Check node type
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(child).__name__}")

        # Special handling for function calls
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names: eval(), exec()
            if isinstance(func, ast.Name) and func.id in DISALLOWED_FUNC_NAMES:
                raise ValueError(f"Disallowed function call: {func.id}()")
            # Handle attribute access like os.system()
            if isinstance(func, ast.Attribute):
                full_name = _get_full_attr_name(func)
                if full_name in DISALLOWED_FUNC_NAMES:
                    raise ValueError(f"Disallowed function call: {full_name}()")

def _get_full_attr_name(node: ast.Attribute) -> str:
    """
    Recursively build the dotted name for an Attribute node.
    """
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))

def process_code_input(code_input: str):
    """
    Execute a small Python snippet in a tightly restricted environment.

    Parameters
    ----------
    code_input : str
        The Python source to run.

    Returns
    -------
    None or str
        If the snippet produces output via print(), that output is returned as a string.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse and validate the code
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    _check_disallowed(parsed)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Capture printed output
    stdout_capture = StringIO()
    with redirect_stdout(stdout_capture):
        try:
            exec(compile(parsed, filename="<sandbox>", mode="exec"), exec_globals, exec_locals)
        except Exception as exc:
            # Re‑raise any runtime errors
            raise ValueError(f"Runtime error: {exc}") from exc

    output = stdout_capture.getvalue()
    return output if output else None
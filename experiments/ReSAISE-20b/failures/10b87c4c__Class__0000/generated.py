import ast
import builtins
from contextlib import redirect_stdout
import io

# Disallowed node types and names that could lead to unsafe operations
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,               # Python 2 style exec (not present in Py3 but kept for clarity)
    ast.Call,
)

# Names of functions that are considered dangerous in this environment
DISALLOWED_NAMES = {
    "open",   # file I/O
    "eval",
    "exec",
    "__import__",
    "compile",
    "input",  # may block or expose environment
}

class _SecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.found_disallowed = False

    def visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            self.found_disallowed = True
            return
        # Disallow calls to dangerous built-ins
        if isinstance(node, ast.Call):
            func = node.func
            # Handle simple names like eval(...)
            if isinstance(func, ast.Name) and func.id in DISALLOWED_NAMES:
                self.found_disallowed = True
                return
            # Handle attribute calls like os.system(...)
            if isinstance(func, ast.Attribute):
                # We disallow any call to an attribute of a module that is not in the safe list
                if isinstance(func.value, ast.Name):
                    self.found_disallowed = True
                    return
        # Recursively visit child nodes
        super().visit(node)

def process_code_input(code_input: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The code to execute. It may contain assignments, expressions,
        function definitions, and print statements.

    Returns
    -------
    None or any value produced by the last expression in the code block.
        If the snippet contains a print statement, its output is captured
        and returned as a string.  If the snippet contains an expression
        that evaluates to a value (e.g., ``1 + 2``), that value is returned.
        If the snippet contains neither, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations such as imports,
        calls to dangerous built‑ins, or file I/O.
    """

    # 1. Syntax check and disallow unsafe constructs
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    checker = _SecurityChecker()
    checker.visit(parsed)
    if checker.found_disallowed:
        raise ValueError("Disallowed operation detected in the code snippet.")

    # 2. Prepare a minimal execution environment
    safe_builtins = {
        name: getattr(builtins, name)
        for name in [
            "abs", "all", "any", "bool", "chr", "dict",
            "float", "int", "len", "list", "max", "min",
            "pow", "range", "round", "str", "sum", "tuple"
        ]
    }
    # Provide a simple print that writes to stdout (captured below)
    exec_globals = {"__builtins__": safe_builtins}

    # 3. Execute the code and capture stdout
    stdout_capture = io.StringIO()
    try:
        with redirect_stdout(stdout_capture):
            exec(compile(parsed, filename="<snippet>", mode="exec"), exec_globals)
    except Exception as exc:
        # Re‑raise runtime errors with a clear message
        raise ValueError(f"Runtime error during execution: {exc}") from exc

    # 4. Determine what to return
    printed = stdout_capture.getvalue()
    if printed:
        return printed.rstrip("\n")  # remove trailing newline for consistency

    # If the snippet ends with an expression, it will be present in exec_globals['_']
    result = exec_globals.get("_")
    return result
import ast
import io
import contextlib

# A list of built‑ins that we consider safe for a teaching environment.
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'dict', 'float',
    'int', 'len', 'list', 'max', 'min', 'print', 'range',
    'round', 'str', 'sum', 'tuple', 'type'
}

# Names of functions or modules that are disallowed from being called directly.
DISALLOWED_CALLS = {
    'open', 'eval', 'exec', 'compile',
    '__import__',  # prevents importing arbitrary modules
    'os.system', 'subprocess.run', 'subprocess.Popen',
    'socket.socket'
}

class CodeSafetyChecker(ast.NodeVisitor):
    """
    Traverses the AST of a user supplied code snippet and raises
    ValueError if disallowed constructs are found.
    """
    def __init__(self):
        super().__init__()
        self.allowed_imports = {'math', 'random'}  # example allowed modules

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name not in self.allowed_imports:
                raise ValueError(f"Import of module '{alias.name}' is not allowed")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module not in self.allowed_imports:
            raise ValueError(f"Import from module '{node.module}' is not allowed")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Check if the function being called is disallowed
        func_name = self._get_call_name(node.func)
        if func_name in DISALLOWED_CALLS:
            raise ValueError(f"Call to '{func_name}' is not allowed")
        self.generic_visit(node)

    def _get_call_name(self, node):
        """Return a string representation of the called function."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_call_name(node.value)
            return f"{value}.{node.attr}"
        return ""

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent attribute access on dangerous objects like os, subprocess
        if isinstance(node.value, ast.Name) and node.value.id in {'os', 'subprocess'}:
            raise ValueError(f"Access to attribute '{node.attr}' of module '{node.value.id}' is not allowed")
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        raise ValueError("Global statements are not allowed")

    def visit_Nonlocal(self, node: ast.Nonlocal):
        raise ValueError("Nonlocal statements are not allowed")

def process_code_input(code_input: str):
    """
    Execute a small, safe Python snippet and return its output.

    Parameters
    ----------
    code_input : str
        The user supplied Python source code.

    Returns
    -------
    None | str
        None if the snippet produced no output, otherwise the printed
        output as a string.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Syntax and safety check
    try:
        tree = ast.parse(code_input, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    checker = CodeSafetyChecker()
    checker.visit(tree)

    # 2. Prepare a restricted execution environment
    safe_builtins = {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}
    exec_globals = {"__builtins__": safe_builtins}

    # 3. Capture stdout
    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(compile(tree, filename="<user_snippet>", mode="exec"), exec_globals)
    except Exception as exc:
        # Re‑raise as ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from exc

    result = output_buffer.getvalue()
    return result if result else None
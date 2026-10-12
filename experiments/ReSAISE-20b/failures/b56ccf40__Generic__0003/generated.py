import ast
import builtins
import sys
from io import StringIO

# -----------------------------------------------------------------------------
# 1. Define a whitelist of safe built‑in names
# -----------------------------------------------------------------------------
SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in (
        # Basic types and constructors
        'int', 'float', 'str', 'bool', 'list', 'dict', 'set',
        # Containers & helpers
        'range', 'enumerate', 'zip', 'map', 'filter',
        # Mathematical functions
        'abs', 'min', 'max', 'sum', 'round',
        # I/O helpers
        'print',
        # Misc
        'len', 'tuple', 'type',
    )
}

# -----------------------------------------------------------------------------
# 2. AST visitor that rejects dangerous constructs
# -----------------------------------------------------------------------------
class SafeNodeVisitor(ast.NodeVisitor):
    """
    Traverses the AST and raises ValueError if a forbidden node is found.
    """

    # Forbidden node types
    FORBIDDEN_NODES = (
        ast.Import,          # import statements
        ast.ImportFrom,
        ast.Exec,            # exec (py2)
        ast.Call,           # function calls – we will check the callee
    )

    # Forbidden function names (as strings)
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'open', 'compile',
        '__import__', 'input', 'globals', 'locals', 'vars',
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden construct: {type(node).__name__}")
        # Special handling for function calls
        if isinstance(node, ast.Call):
            self._check_call(node)
        super().visit(node)

    def _check_call(self, node):
        # Resolve the function name if it's a simple Name
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # disallow attribute access (e.g., obj.attr())
            raise ValueError("Attribute access is forbidden")
        if func_name in self.FORBIDDEN_CALLS:
            raise ValueError(f"Forbidden function call: {func_name}")

# -----------------------------------------------------------------------------
# 3. The main sandboxed execution routine
# -----------------------------------------------------------------------------
def process_user_code(code_submission: str):
    """
    Safely executes a user‑supplied Python script.

    Parameters
    ----------
    code_submission : str
        The source code to run.

    Returns
    -------
    str | None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains syntax errors or forbidden operations.
    """

    # 3.1 Parse and validate the AST
    try:
        tree = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # 3.2 Walk the tree to detect unsafe constructs
    SafeNodeVisitor().visit(tree)

    # 3.3 Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # 3.4 Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    try:
        sys.stdout = fake_out
        # Compile and execute the code in the restricted environment
        compiled_code = compile(tree, filename="<user_script>", mode="exec")
        exec(compiled_code, safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None
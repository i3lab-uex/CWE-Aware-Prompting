import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# List of forbidden AST node types or attributes
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # Python 2 only – kept for completeness
    ast.Call,
)

# Functions and names that are explicitly disallowed in calls
FORBIDDEN_CALLS = {
    "__import__",
    "eval",
    "exec",
    "open",
}

# Names of modules that should not be imported or accessed
FORBIDDEN_MODULES = {
    "os",
    "sys",
    "subprocess",
    "socket",
    "shutil",
}

class SecurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        # Reject any forbidden node type
        if isinstance(node, FORBIDDEN_NODES):
            self.errors.append(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Check the function being called
        func_name = self._get_call_func_name(node)
        if func_name in FORBIDDEN_CALLS:
            self.errors.append(f"Disallowed function call: {func_name}")
        super().visit_Call(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split('.')[0] in FORBIDDEN_MODULES:
                self.errors.append(f"Disallowed import of module: {alias.name}")
        super().visit_Import(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split('.')[0] in FORBIDDEN_MODULES:
            self.errors.append(f"Disallowed import from module: {node.module}")
        super().visit_ImportFrom(node)

    def _get_call_func_name(self, node):
        """
        Resolve the name of the function being called.
        Supports simple names and attribute accesses like os.system.
        """
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            # For attribute accesses, get the top-level name
            attr_chain = []
            current = node.func
            while isinstance(current, ast.Attribute):
                attr_chain.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                attr_chain.append(current.id)
                # The first element is the base name
                return '.'.join(reversed(attr_chain))
        return ""

def run_code_snippet(snippet: str):
    """
    Execute a small Python snippet in a sandboxed environment.
    Raises ValueError if the code contains disallowed operations.
    Returns None if nothing is produced, otherwise returns a value
    assigned to the variable 'result' by the snippet.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Perform security checks
    checker = SecurityChecker()
    checker.visit(tree)
    if checker.errors:
        raise ValueError(f"Disallowed code detected: {', '.join(checker.errors)}")

    # Prepare a restricted global namespace
    safe_builtins = {k: v for k, v in builtins.__dict__.items()
                     if k in ('abs', 'all', 'any', 'bool',
                              'chr', 'dict', 'float', 'int', 'len',
                              'list', 'max', 'min', 'pow', 'range',
                              'round', 'str', 'sum', 'tuple')}
    globals_dict = {"__builtins__": safe_builtins}

    # Capture stdout
    output_buffer = StringIO()
    with redirect_stdout(output_buffer):
        exec(compile(tree, filename="<snippet>", mode="exec"), globals_dict)

    # If the snippet produced output on stdout, return it
    captured = output_buffer.getvalue()
    if captured:
        return captured.strip()

    # If the snippet assigned a variable named 'result', return it
    if "result" in globals_dict:
        return globals_dict["result"]

    # Otherwise, nothing to return
    return None
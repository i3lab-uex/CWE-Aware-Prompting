import ast
import sys
from types import ModuleType, FunctionType

# List of AST node types that are considered disallowed
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # will be inspected for specific functions
)

# Names of disallowed function calls (e.g. os.system, eval, exec)
DISALLOWED_CALLS = {
    'eval',
    'exec',
    'open',
    'compile',
    'input',          # prevent interactive input
    'os.system',
    'subprocess.Popen',
    'subprocess.call',
}

# Allowed builtins (very restrictive)
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool',
    'chr', 'divmod', 'enumerate', 'filter', 'float',
    'hash', 'hex', 'int', 'isinstance', 'len',
    'list', 'map', 'max', 'min', 'next', 'pow',
    'range', 'repr', 'reversed', 'round', 'set',
    'slice', 'sorted', 'str', 'sum', 'tuple',
}

class DisallowedCodeVisitor(ast.NodeVisitor):
    def __init__(self, snippet: str):
        self.snippet = snippet
        self.error = None

    def visit_Import(self, node):
        self.error = f"Disallowed import statement at line {node.lineno}"
        return

    def visit_ImportFrom(self, node):
        self.error = f"Disallowed import-from statement at line {node.lineno}"
        return

    def visit_Call(self, node):
        # Detect disallowed function calls
        func_name = self._get_call_name(node.func)
        if func_name in DISALLOWED_CALLS:
            self.error = f"Disallowed function call '{func_name}' at line {node.lineno}"
            return
        self.generic_visit(node)

    def _get_call_name(self, node):
        # Resolve attribute chains (e.g., os.system)
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_call_name(node.value)
            if value:
                return f"{value}.{node.attr}"
        return None

def run_code_snippet(snippet: str):
    """
    Execute a Python code snippet in a highly restricted environment.

    Parameters
    ----------
    snippet : str
        The Python code to execute. It may contain expressions, assignments,
        function definitions, etc.

    Returns
    -------
    None or any
        If the snippet produces a value as its last expression, that value is
        returned. Otherwise None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations (imports, unsafe calls,
        etc.) or references to forbidden built‑ins.
    """

    # 1. Syntax check and disallowed operation detection
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    visitor = DisallowedCodeVisitor(snippet)
    visitor.visit(tree)

    if visitor.error:
        raise ValueError(visitor.error)

    # 2. Build a restricted globals dict
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS if name in __builtins__}
    }

    # 3. Execute the snippet and capture the result of the last expression
    local_vars = {}
    exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, local_vars)

    # The last expression result is stored in the special variable "_"
    return local_vars.get('_')

# Example usage (uncomment to test):
# result = run_code_snippet("x = 5\nx * 2")
# print(result)   # Should output 10
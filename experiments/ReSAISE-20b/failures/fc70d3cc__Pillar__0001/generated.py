import ast
import builtins
import io
import sys

# ------------------------------------------------------------
#  Safe execution environment
# ------------------------------------------------------------

# Whitelist of safe built‑in functions / objects
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'set': set,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # Add more as needed
}

# ------------------------------------------------------------------
#  AST visitor to detect forbidden constructs
# ------------------------------------------------------------------

class SafeNodeVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if any forbidden node is found.
    """

    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # Calls are inspected for dangerous functions
        ast.Exec,          # Python 2 legacy (kept for completeness)
        ast.Global,
        ast.Nonlocal,
        ast.With,          # Prevent use of context managers that might open files
    )

    DANGEROUS_FUNCTIONS = {
        'open', 'exec', 'eval', 'compile', '__import__',
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Check if the function called is dangerous
        func_name = self._get_call_func_name(node.func)
        if func_name in self.DANGEROUS_FUNCTIONS:
            raise ValueError(f"Call to dangerous function '{func_name}' is not allowed")
        self.generic_visit(node)

    def _get_call_func_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # For calls like obj.open() we disallow any attribute named open
            return node.attr
        return ""

# ------------------------------------------------------------------
#  Main execution function
# ------------------------------------------------------------------

def execute_python_code(snippet_code: str):
    """
    Safely executes a snippet of Python code.

    Parameters
    ----------
    snippet_code : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any
        Result of the last expression if any, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    # 1. Syntax check and AST validation
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}") from None

    # 2. Walk the AST for forbidden nodes
    SafeNodeVisitor().visit(parsed)

    # 3. Prepare restricted globals and locals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # 4. Capture stdout to prevent unintended printing
    old_stdout = sys.stdout
    stdout_capture = io.StringIO()
    sys.stdout = stdout_capture

    try:
        # Compile the code
        compiled = compile(parsed, filename="<user_snippet>", mode="exec")
        # Execute in the safe environment
        exec(compiled, safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 5. Determine a return value: if the user defined a variable named "__result__",
    #    we return it; otherwise None.
    return safe_locals.get("__result__", None)
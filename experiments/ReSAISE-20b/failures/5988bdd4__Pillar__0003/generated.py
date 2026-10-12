import ast
import sys
from io import StringIO

# ----------------------------------------------------------------------
# Safe sandbox for executing user‑supplied Python snippets
# ----------------------------------------------------------------------
class _SafeNodeVisitor(ast.NodeVisitor):
    """
    AST visitor that rejects disallowed nodes and function calls.
    Raises ValueError on forbidden constructs.
    """
    # Disallowed node types
    _disallowed_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
        ast.Try,
        ast.ExceptHandler,
    )

    # Disallowed function names (built‑in)
    _disallowed_calls = {
        'open', 'exec', 'eval', 'compile',
        '__import__', 'input', 'locals', 'globals',
    }

    def visit(self, node):
        if isinstance(node, self._disallowed_nodes):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Reject calls to disallowed built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in self._disallowed_calls:
            raise ValueError(f"Disallowed function call: {node.func.id}")
        # Reject calls to attributes (e.g., os.system)
        if isinstance(node.func, ast.Attribute):
            raise ValueError("Disallowed attribute call")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent attribute access on arbitrary objects
        raise ValueError(f"Disallowed attribute access: {ast.dump(node)}")

    def visit_Subscript(self, node: ast.Subscript):
        # Allow subscript but only on allowed names
        if isinstance(node.value, ast.Name) and node.value.id not in _ALLOWED_GLOBALS:
            raise ValueError(f"Disallowed subscript on {node.value.id}")
        self.generic_visit(node)

# ----------------------------------------------------------------------
# Allowed built‑ins and globals
# ----------------------------------------------------------------------
_ALLOWED_GLOBALS = {
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'sum': sum,
    'min': min,
    'max': max,
}

def _prepare_globals():
    return {
        '__builtins__': {},  # empty built‑in namespace
        **_ALLOWED_GLOBALS,
    }

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def run_python_snippet(snippet_string: str):
    """
    Execute a Python snippet safely.

    Parameters
    ----------
    snippet_string : str
        The user supplied code to execute.

    Returns
    -------
    object or None
        Result of the snippet if it evaluates an expression, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    if not isinstance(snippet_string, str):
        raise ValueError("snippet_string must be a string")

    # Parse the snippet and perform safety checks
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Walk the AST to ensure safety
    _SafeNodeVisitor().visit(parsed)

    # Prepare restricted environment
    globals_dict = _prepare_globals()
    locals_dict = {}

    # Capture stdout to detect print statements
    old_stdout = sys.stdout
    fake_out = StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(parsed, filename="<snippet>", mode="exec"), globals_dict, locals_dict)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # If the snippet ends with an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the last expression in the same context
        try:
            expr_code = compile(ast.Expression(parsed.body[-1].value), filename="<expr>", mode="eval")
            return eval(expr_code, globals_dict, locals_dict)
        except Exception as exc:
            raise ValueError(f"Expression evaluation error: {exc}") from exc

    # If there is a variable named 'result', return it
    if 'result' in locals_dict:
        return locals_dict['result']

    # No explicit result; return None
    return None
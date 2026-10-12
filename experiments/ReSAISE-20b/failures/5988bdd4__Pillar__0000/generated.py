import ast
import sys
from io import StringIO

# ------------------------------------------------------------
# Helper: detect forbidden nodes in the AST
# ------------------------------------------------------------
FORBIDDEN_NAMES = {
    # Built‑in functions that can access the system
    "open", "exec", "eval", "__import__", "input",
    # Common modules that expose dangerous functions
    "os", "subprocess", "sys", "shutil",
}

# Disallowed attribute chains (e.g., os.system)
FORBIDDEN_ATTRS = {
    ("os", "system"),
    ("subprocess", "Popen"),
}

def _is_forbidden_call(node: ast.Call) -> bool:
    """Return True if the Call node invokes a forbidden name or attribute."""
    # Direct call to a name
    if isinstance(node.func, ast.Name):
        return node.func.id in FORBIDDEN_NAMES

    # Call to an attribute (e.g., os.system)
    if isinstance(node.func, ast.Attribute):
        # Resolve the base name
        if isinstance(node.func.value, ast.Name):
            base = node.func.value.id
            attr = node.func.attr
            return (base, attr) in FORBIDDEN_ATTRS or base in FORBIDDEN_NAMES
    return False

def _check_ast(tree: ast.AST):
    """Walk the AST and raise ValueError if forbidden constructs are found."""
    for node in ast.walk(tree):
        # Imports
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are forbidden.")
        # Calls to dangerous functions
        if isinstance(node, ast.Call) and _is_forbidden_call(node):
            raise ValueError(f"Forbidden function call detected: {ast.dump(node)}")
        # Attribute access to dangerous modules
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id in FORBIDDEN_NAMES:
                raise ValueError(f"Forbidden attribute access: {node.value.id}.{node.attr}")

# ------------------------------------------------------------
# Restricted globals for exec/eval
# ------------------------------------------------------------
SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
}

SAFE_GLOBALS = {"__builtins__": SAFE_BUILTINS}

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------
def run_python_snippet(snippet_string: str):
    """
    Execute a user-provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_string : str
        The code to execute.

    Returns
    -------
    Any
        The result of evaluating the snippet if it is an expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    if not isinstance(snippet_string, str):
        raise ValueError("snippet_string must be a string")

    # Parse the snippet into an AST
    try:
        tree = ast.parse(snippet_string, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Check for forbidden constructs
    _check_ast(tree)

    # Prepare a StringIO to capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Try to compile as an expression first
        try:
            expr_tree = ast.parse(snippet_string, mode="eval")
            compiled_expr = compile(expr_tree, filename="<snippet>", mode="eval")
            result = eval(compiled_expr, SAFE_GLOBALS)
        except SyntaxError:
            # Not a single expression; execute as statements
            compiled_code = compile(tree, filename="<snippet>", mode="exec")
            exec(compiled_code, SAFE_GLOBALS)
            result = None
    finally:
        # Restore original stdout
        sys.stdout = old_stdout

    return result
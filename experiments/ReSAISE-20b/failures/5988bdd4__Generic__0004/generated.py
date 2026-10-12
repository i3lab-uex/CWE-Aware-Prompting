import ast
import builtins
import io
import sys

# Define a list of AST node types that are considered unsafe.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 only, but keep for completeness
    ast.Call,           # We'll filter calls to builtins explicitly
    ast.Attribute,
    ast.Subscript,
    ast.Name,           # We'll allow names that are safe
)

# Whitelist of allowed builtins for the sandbox.
SAFE_BUILTINS = {
    'print': print,
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
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Ensure that a function call is to an allowed builtin only.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id in SAFE_BUILTINS
    # Disallow attribute calls (e.g., os.system)
    return False

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any forbidden
    construct is found.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node type: {type(child).__name__}")
        if isinstance(child, ast.Call) and not _is_safe_call(child):
            raise ValueError(f"Call to forbidden function: {ast.dump(child)}")
        _check_ast(child)

def run_python_snippet(snippet_string: str):
    """
    Execute a user-provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_string : str
        The code to be executed.

    Returns
    -------
    Any
        The value produced by the snippet if it contains an expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is invalid.
    """
    # Parse the code and validate it
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    _check_ast(parsed)

    # Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Capture stdout to detect print output
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # If the snippet is a single expression, evaluate it
        if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
            expr_value = eval(compile(parsed, filename="<snippet>", mode="eval"),
                              sandbox_globals, sandbox_locals)
            output = fake_out.getvalue()
            return expr_value if output == "" else output
        else:
            exec(compile(parsed, filename="<snippet>", mode="exec"),
                 sandbox_globals, sandbox_locals)
            output = fake_out.getvalue()
            return output if output else None
    finally:
        sys.stdout = old_stdout

# Example usage (uncomment to test)
# print(run_python_snippet("2 + 3"))          # Should return 5
# print(run_python_snippet("print('Hello')")) # Should return 'Hello\n'
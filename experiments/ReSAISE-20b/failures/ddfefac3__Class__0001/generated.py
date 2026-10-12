import ast
from contextlib import redirect_stdout
import io

# List of AST node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,            # Python 2 only; kept for completeness
    ast.Call,            # Calls are allowed but we will filter dangerous ones
)

# Disallowed function names that can perform unsafe operations
DISALLOWED_CALLS = {
    'open',
    'eval',
    'exec',          # built-in exec is a function in Python 3
    '__import__',
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the function being called is not in DISALLOWED_CALLS.
    Handles both direct calls and attribute accesses (e.g., os.system).
    """
    # Function can be a Name or an Attribute
    if isinstance(node.func, ast.Name):
        return node.func.id not in DISALLOWED_CALLS
    if isinstance(node.func, ast.Attribute):
        # For attribute calls we disallow any chain that contains a disallowed base
        attr_chain = []
        current = node.func
        while isinstance(current, ast.Attribute):
            attr_chain.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            attr_chain.append(current.id)
        # If any part of the chain is disallowed, reject
        return not any(part in DISALLOWED_CALLS for part in attr_chain)
    return False

def _validate_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if an unsafe construct is found.
    """
    for child in ast.walk(node):
        if isinstance(child, UNSAFE_NODES):
            raise ValueError(f"Use of '{child.__class__.__name__}' is forbidden.")
        if isinstance(child, ast.Call) and not _is_safe_call(child):
            raise ValueError(f"Call to '{ast.unparse(child.func)}' is forbidden.")
        # Disallow attribute access to builtins (e.g., __builtins__.__dict__)
        if isinstance(child, ast.Attribute):
            if (
                isinstance(child.value, ast.Name)
                and child.value.id in ('__builtins__', 'builtins')
            ):
                raise ValueError("Direct access to builtins is forbidden.")

def process_python_code(code_str: str):
    """
    Execute user-provided Python code in a restricted environment.
    
    Parameters
    ----------
    code_str : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any
        The value of the last expression in the snippet, if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet attempts forbidden operations or contains invalid code.
    """
    # Parse the source to an AST
    try:
        tree = ast.parse(code_str, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")

    # Validate the AST for unsafe patterns
    _validate_ast(tree)

    # Prepare a restricted global namespace
    safe_globals = {
        "__builtins__": {},   # No built‑in functions or modules
    }
    safe_locals = {}

    # Capture stdout to avoid leaking output
    stdout_buffer = io.StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(tree, filename="<user_code>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # Determine the value of the last expression, if present
    last_expr = None
    for node in reversed(tree.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the restricted context
            try:
                last_expr = eval(compile(ast.Expression(node.value), filename="<user_code>", mode="eval"),
                                 safe_globals, safe_locals)
            except Exception:
                pass
            break

    return last_expr if last_expr is not None else None
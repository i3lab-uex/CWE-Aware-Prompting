import ast
from types import SimpleNamespace

# List of disallowed node types and built‑in functions for a minimal sandbox
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls are allowed only to safe builtins
    ast.Attribute,     # disallow attribute access (e.g., os.system)
)

SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'complex': complex,
    'dict': dict,
    'divmod': divmod,
    'float': float,
    'hash': hash,
    'hex': hex,
    'int': int,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'repr': repr,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # allow basic math functions
    'math': __import__('math'),
}

# Whitelist of safe function names that may be called
SAFE_FUNCTIONS = {
    'abs', 'all', 'any', 'bool', 'chr', 'complex',
    'dict', 'divmod', 'float', 'hash', 'hex', 'int',
    'len', 'list', 'map', 'max', 'min', 'pow',
    'range', 'repr', 'round', 'str', 'sum', 'tuple',
}

def _check_syntax_and_security(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any disallowed construct
    is found.
    """
    for child in ast.walk(node):
        # Reject import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed")

        # Reject attribute access (e.g., os.system)
        if isinstance(child, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

        # Reject function calls to non‑safe builtins
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names (e.g., print)
            if isinstance(func, ast.Name):
                name = func.id
                if name not in SAFE_FUNCTIONS and name != 'print':
                    raise ValueError(f"Call to unsafe function '{name}' is not allowed")
            else:
                # Any complex call (e.g., obj.method()) is forbidden
                raise ValueError("Complex function calls are not allowed")

def run_python_snippet(snippet_string: str):
    """
    Execute a user provided Python snippet in a heavily restricted sandbox.

    Parameters
    ----------
    snippet_string : str
        The code to execute. It may contain expressions or statements.

    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if no
        expression produced a value.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or attempts forbidden actions.
    """
    if not isinstance(snippet_string, str):
        raise ValueError("snippet_string must be a string")

    # Parse the snippet into an AST
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Security checks
    _check_syntax_and_security(parsed)

    # Prepare a minimal global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Execute the code
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # Retrieve the value of the last expression if it exists
    # We look for a Name node that is assigned in the last statement
    last_value = None
    for stmt in reversed(parsed.body):
        if isinstance(stmt, ast.Expr):
            # Evaluate the expression in the sandbox context
            expr_code = compile(ast.Expression(stmt.value), filename="<sandbox>", mode="eval")
            last_value = eval(expr_code, sandbox_globals, sandbox_locals)
            break
        elif isinstance(stmt, (ast.Assign, ast.AugAssign)):
            # The value of the target variable is returned if it's a simple name
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            for t in targets:
                if isinstance(t, ast.Name):
                    last_value = sandbox_locals.get(t.id)
                    break
            if last_value is not None:
                break

    return last_value
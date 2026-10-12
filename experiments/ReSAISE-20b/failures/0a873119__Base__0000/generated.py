import ast
import builtins
from types import SimpleNamespace

# List of disallowed AST node types
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,              # Python 2
    ast.Call,              # We'll inspect calls separately
}

# Disallowed function names that could be used for side‑effects
DISALLOWED_CALLS = {
    'open',
    'exec',
    'eval',
    'compile',
    'input',
    # OS and subprocess modules
    'system',
    'popen',
    'subprocess',
    # built‑in functions that may be overridden
    '__import__',
}

# Allowed builtins for the sandbox
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
}

def _check_ast(node):
    """
    Recursively walk the AST and raise ValueError if a disallowed
    construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are prohibited")

        # Disallow exec/eval/compile calls
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names: open(), eval() ...
            if isinstance(func, ast.Name) and func.id in DISALLOWED_CALLS:
                raise ValueError(f"Call to prohibited function '{func.id}'")
            # Handle attribute calls: os.system(), subprocess.Popen()
            if isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in DISALLOWED_CALLS:
                    raise ValueError(f"Call to prohibited attribute '{attr_name}'")
                # Reject calls on any module that could be dangerous
                if isinstance(func.value, ast.Name) and func.value.id in {'os', 'subprocess'}:
                    raise ValueError(f"Call to prohibited module '{func.value.id}.{attr_name}'")

        # Recursively check children
        _check_ast(child)

def safe_run_script(script_code: str):
    """
    Execute a user supplied Python script in a restricted environment.
    Returns the value of the last expression, or None if no result.
    Raises ValueError on prohibited operations or syntax errors.
    """
    # Parse the script to catch syntax errors early
    try:
        parsed = ast.parse(script_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from None

    # Validate AST for disallowed constructs
    _check_ast(parsed)

    # Prepare the sandboxed globals and locals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Execute the script
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"),
             sandbox_globals,
             sandbox_locals)
    except Exception as exc:
        # Wrap any runtime exception in ValueError to keep API consistent
        raise ValueError(f"Runtime error: {exc}") from None

    # Attempt to return the value of the last expression if present
    # The parsed body may end with an Expr node; fetch its value
    last_expr = None
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in sandboxed context
            try:
                last_expr = eval(compile(ast.Expression(node.value),
                                         filename="<sandbox>",
                                         mode="eval"),
                                 sandbox_globals,
                                 sandbox_locals)
            except Exception:
                pass
            break

    return last_expr if last_expr is not None else None
import ast
import builtins

# List of safe built-in functions and constants that we expose to the snippet.
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
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # add more as needed
}

# AST nodes that are disallowed in the snippet.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,           # disallow any function call (we can allow specific safe calls)
    ast.Exec,
    ast.Global,         # global variables are not allowed
    ast.Nonlocal,
    ast.With,
    ast.Try,            # try/except can be dangerous
    ast.Lambda,
    ast.AsyncFunctionDef,
    ast.FunctionDef,    # no user defined functions
    ast.ClassDef,
    ast.Attribute,      # accessing attributes like os.system
)

# Allowed function calls (by name). Everything else is blocked.
ALLOWED_CALLS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float',
    'int', 'len', 'list', 'max', 'min', 'pow',
    'range', 'round', 'str', 'sum', 'tuple'
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a forbidden node is found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow imports, globals, etc.
        if isinstance(child, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden construct: {type(child).__name__}")

        # Disallow function calls that are not in the whitelist.
        if isinstance(child, ast.Call):
            # Only allow calls to whitelisted builtins
            if isinstance(child.func, ast.Name):
                if child.func.id not in ALLOWED_CALLS:
                    raise ValueError(f"Call to disallowed function: {child.func.id}")
            else:
                # Any other call (e.g., attribute access) is disallowed
                raise ValueError("Only simple function calls to whitelisted names are allowed")

        _check_ast(child)

def run_python_snippet(snippet_string: str):
    """
    Safely execute a short Python snippet.

    Parameters
    ----------
    snippet_string : str
        The user supplied code to execute.

    Returns
    -------
    Any
        The result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed constructs or is syntactically invalid.
    """
    try:
        # Parse the snippet into an AST
        tree = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Validate the AST
    _check_ast(tree)

    # Prepare a restricted execution environment.
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # If the snippet is a single expression, evaluate it.
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        expr_code = compile(ast.Expression(body=tree.body[0].value), "<string>", "eval")
        return eval(expr_code, exec_globals, exec_locals)

    # Otherwise execute the statements and return None.
    compiled = compile(tree, "<string>", "exec")
    exec(compiled, exec_globals, exec_locals)
    return None
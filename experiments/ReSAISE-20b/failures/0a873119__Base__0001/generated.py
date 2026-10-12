import ast
from types import CodeType, FunctionType

# ----------------------------------------------------------------------
# Safe execution environment
# ----------------------------------------------------------------------
SAFE_BUILTINS = {
    # basic functions that are generally safe
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
    'sorted': sorted,
    # constants
    'True': True,
    'False': False,
    'None': None,
}

# ----------------------------------------------------------------------
# Disallowed AST node types
# ----------------------------------------------------------------------
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2
    ast.Call,          # calls to functions that are not whitelisted
    ast.Attribute,
    ast.Global,
    ast.Nonlocal,
    ast.With,
    ast.Try,
    ast.Lambda,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
}

# Disallowed function names (to be checked only when a Call node is encountered)
DISALLOWED_FUNC_NAMES = {
    'open', 'exec', 'eval', '__import__',
    # common dangerous modules
    'subprocess', 'os', 'sys', 'socket', 'pickle',
}

# ----------------------------------------------------------------------
def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the call is to a whitelisted built-in or
    a lambda defined in the user code.  Any other call is disallowed.
    """
    # Only allow calls to names that are in SAFE_BUILTINS
    if isinstance(node.func, ast.Name):
        return node.func.id in SAFE_BUILTINS and node.func.id not in DISALLOWED_FUNC_NAMES
    # For attribute calls (e.g. obj.method()), disallow entirely
    return False

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a disallowed
    construct is found.
    """
    for child in ast.walk(node):
        # Disallow certain node types outright
        if type(child) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")

        # Disallow calls to unsafe functions
        if isinstance(child, ast.Call):
            if not _is_safe_call(child):
                raise ValueError(f"Disallowed function call: {ast.unparse(child)}")

        # Disallow any use of 'import' statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed")

        # Disallow use of 'exec' or 'eval'
        if isinstance(child, ast.Name) and child.id in ('exec', 'eval'):
            raise ValueError(f"Use of '{child.id}' is prohibited")

        # Disallow writing to globals
        if isinstance(child, ast.Global) or isinstance(child, ast.Nonlocal):
            raise ValueError("Global/Nonlocal assignments are prohibited")

        # Disallow defining functions or classes
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            raise ValueError("Defining functions or classes is prohibited")

def safe_run_script(script_code: str):
    """
    Execute a user‑supplied Python script in a restricted environment.

    Parameters
    ----------
    script_code : str
        The user supplied code to execute.

    Returns
    -------
    Any
        If the script ends with an expression, its value is returned.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the code contains prohibited syntax or unsafe operations.
    SyntaxError
        If the supplied code is not valid Python syntax.
    """
    # Parse the script and validate the AST
    try:
        parsed = ast.parse(script_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    _check_ast(parsed)

    # Determine if the last statement is an expression
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Compile as an expression
        expr_code: CodeType = compile(parsed.body[-1], '<string>', mode='eval')
        result = eval(expr_code, {'__builtins__': SAFE_BUILTINS}, {})
    else:
        # Compile as a normal script
        exec_code: CodeType = compile(parsed, '<string>', mode='exec')
        local_vars = {}
        exec(exec_code, {'__builtins__': SAFE_BUILTINS}, local_vars)
        result = None

    return result
import ast
import io
import sys
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# 1. Whitelist of safe built‑in functions
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
    'sum': sum,
    'min': min,
    'max': max,
}

# --------------------------------------------------------------------------- #
# 2. Allowed AST node types
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Import,  # allow import of safe modules only
    ast.ImportFrom,
    ast.FunctionDef,
    ast.Return,
    ast.Assign,
    ast.AugAssign,
    ast.For,
    ast.While,
    ast.If,
    ast.Break,
    ast.Continue,
    ast.Pass,
    ast.Expr,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Del,
    ast.Constant,
    ast.Num,  # deprecated but for Python <3.8
    ast.Str,  # deprecated but for Python <3.8
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.UnaryOp,
    ast.BinOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.Slice,
)

# --------------------------------------------------------------------------- #
# 3. Names that are explicitly forbidden
FORBIDDEN_NAMES = {
    'eval',
    'exec',
    'open',
    '__import__',
    'compile',
    'input',
    'help',
}

# --------------------------------------------------------------------------- #
# 4. Helper to walk the AST and validate
def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if any disallowed
    construct is encountered.
    """
    for child in ast.walk(node):
        if not isinstance(child, ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(child).__name__}")

        # Disallow certain function names
        if isinstance(child, ast.Name):
            if child.id in FORBIDDEN_NAMES:
                raise ValueError(f"Use of forbidden name '{child.id}' is not allowed")

        # Disallow attribute access to dangerous modules
        if isinstance(child, ast.Attribute):
            if (isinstance(child.value, ast.Name) and child.value.id == 'os') or \
               (isinstance(child.value, ast.Attribute) and getattr(child.value, 'attr', '') == 'system'):
                raise ValueError("Access to os.system or similar is forbidden")

        # Disallow imports of non‑safe modules
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            for alias in getattr(child, 'names', []):
                module_name = alias.name.split('.')[0]
                if module_name not in {'math', 'random'}:  # extend whitelist as needed
                    raise ValueError(f"Import of module '{module_name}' is forbidden")

# --------------------------------------------------------------------------- #
# 5. Main function
def execute_python_code(snippet_code: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet_code : str
        The code to execute.

    Returns
    -------
    Any
        The value of the last expression if present; otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or is syntactically invalid.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Validate the AST
    _validate_ast(parsed)

    # Prepare a restricted global namespace
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}

    # Capture stdout
    old_stdout = sys.stdout
    out_buffer = io.StringIO()
    sys.stdout = out_buffer

    try:
        # Compile and execute the code
        compiled = compile(parsed, '<sandbox>', 'exec')
        exec(compiled, sandbox_globals)

        # Determine the value of the last expression if any
        # We look for the last Expr node in the body
        last_expr_value = None
        for node in reversed(parsed.body):
            if isinstance(node, ast.Expr):
                expr_code = compile(ast.Expression(body=node.value), '<sandbox>', 'eval')
                last_expr_value = eval(expr_code, sandbox_globals)
                break

        # If the snippet printed something, we return that output as a string
        stdout_output = out_buffer.getvalue()
        if stdout_output:
            return stdout_output.rstrip('\n')
        # Else return the value of last expression if present
        return last_expr_value

    finally:
        # Restore stdout regardless of success/failure
        sys.stdout = old_stdout
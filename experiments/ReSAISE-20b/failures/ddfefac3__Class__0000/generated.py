import ast
import builtins
import sys
import io
from types import SimpleNamespace

# List of safe built‑in functions / objects
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
    'repr': repr,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
}

# Forbidden AST node types
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # exec is not a node in Python3 but keep for completeness
    ast.Call,
    ast.Attribute,  # disallow attribute access (e.g., os.system)
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.AsyncFunctionDef,
    ast.Yield,
    ast.YieldFrom,
    ast.Await,
    ast.Global,
    ast.Nonlocal,
}

def _check_ast(tree: ast.AST):
    """
    Walk the AST and raise ValueError if any forbidden node is found.
    Also disallow calls to builtins that are not in SAFE_BUILTINS.
    """
    for node in ast.walk(tree):
        if isinstance(node, tuple(FORBIDDEN_NODES)):
            raise ValueError(f"Forbidden operation: {type(node).__name__}")

        # Disallow calls to unsafe builtins
        if isinstance(node, ast.Call):
            func = node.func
            # direct builtin call: name
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Use of unsafe builtin '{func.id}' is forbidden")
            # attribute access e.g., os.system
            elif isinstance(func, ast.Attribute):
                raise ValueError("Attribute access is forbidden")
    return True

def process_python_code(code_str: str):
    """
    Execute user supplied Python code in a sandboxed environment.
    Returns the value of the last expression if any, otherwise None.

    Raises ValueError for syntax errors or forbidden operations.
    """
    # Parse the code to an AST and validate
    try:
        tree = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}")

    _check_ast(tree)

    # Prepare a restricted global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    result = None
    try:
        # Execute the code
        exec(compile(tree, filename="<sandbox>", mode="exec"),
             sandbox_globals, sandbox_locals)

        # If the last statement is an expression, capture its value
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            expr = tree.body[-1].value
            # Compile the expression separately
            expr_code = compile(ast.Expression(expr), filename="<sandbox>", mode="eval")
            result = eval(expr_code, sandbox_globals, sandbox_locals)

        # If nothing printed and no expression result, return None
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # If something was printed, return the captured output
    out_text = fake_out.getvalue()
    if out_text:
        return out_text.rstrip("\n")
    return result
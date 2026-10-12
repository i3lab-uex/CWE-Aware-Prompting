import ast
import sys
import io
from types import ModuleType, FunctionType

# --------------------------------------------------------------------------- #
# 1. AST-based static analysis – detect disallowed constructs
# --------------------------------------------------------------------------- #

FORBIDDEN_NODES = {
    ast.Import, ast.ImportFrom,      # no imports
    ast.Exec,                        # Python 2 legacy
    ast.Global, ast.Nonlocal,        # variable scope manipulation
    ast.With,                        # with statements
    ast.Try, ast.TryFinally,         # try/except/finally
    ast.Lambda,                      # lambda expressions
    ast.Await, ast.Yield,            # async/await or generators
}

# Disallow use of certain built‑in functions that could be dangerous
DISALLOWED_BUILTINS = {
    "open", "exec", "eval", "compile",
    "input", "__import__", "os", "sys", "subprocess"
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a forbidden node or
    disallowed builtin is found.
    """
    for child in ast.walk(node):
        if isinstance(child, tuple(FORBIDDEN_NODES)):
            raise ValueError(f"Forbidden statement detected: {type(child).__name__}")

        # Check for calls to disallowed builtins
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name) and func.id in DISALLOWED_BUILTINS:
                raise ValueError(f"Disallowed builtin used: {func.id}")

        # Detect attribute access that could reach dangerous modules
        if isinstance(child, ast.Attribute):
            if isinstance(child.value, ast.Name) and child.value.id in {"os", "sys"}:
                raise ValueError(f"Attribute access on {child.value.id} is forbidden")

# --------------------------------------------------------------------------- #
# 2. Execution environment – safe globals & locals
# --------------------------------------------------------------------------- #

SAFE_BUILTINS = {
    # Provide only a very small subset of safe builtins
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    # Arithmetic operators
    "__builtins__": None,  # prevent direct access to all builtins
}

def _create_safe_namespace() -> dict:
    """
    Return a namespace dictionary that will be used as globals during exec.
    """
    return {"__builtins__": SAFE_BUILTINS}

# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #

def process_python_code(code_str: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    code_str : str
        Python source code to be executed.

    Returns
    -------
    result : Any | None
        The value of the last expression in the snippet, or None if there is no
        expression producing a result.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or syntax errors.
    """
    # 1. Parse & statically analyze
    try:
        parsed = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    _check_ast(parsed)

    # 2. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    # 3. Execute
    namespace = _create_safe_namespace()
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"), namespace)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # 4. Retrieve the result of the last expression, if any
    #   We can detect it by checking the AST for Expr nodes at the top level.
    last_expr_value = None
    expr_nodes = [node for node in parsed.body if isinstance(node, ast.Expr)]
    if expr_nodes:
        last_expr = expr_nodes[-1]
        # Compile the expression separately to evaluate it
        try:
            code_obj = compile(ast.Expression(last_expr.value), filename="<sandbox>", mode="eval")
            last_expr_value = eval(code_obj, namespace)
        except Exception:
            # If evaluation fails, ignore and return None
            last_expr_value = None

    # 5. Return the result (or None)
    return last_expr_value
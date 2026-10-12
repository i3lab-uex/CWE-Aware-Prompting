import ast
import sys
import io
from types import FunctionType, CodeType

# List of AST node types that are considered unsafe.
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                # Python 2 only – kept for completeness
    ast.Call,                # Calls to arbitrary functions are disallowed
)

# Disallow calls to dangerous built‑ins or external modules.
DISALLOWED_BUILTINS = {
    "open",
    "eval",
    "exec",
    "compile",
    "input",
    "__import__",
    "globals",
    "locals",
    "vars",
}

# Restrict the set of built‑ins that can be used.
SAFE_BUILTINS = {
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
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

class UnsafeCodeError(ValueError):
    """Raised when the supplied code contains disallowed constructs."""
    pass

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise UnsafeCodeError if an unsafe node is found.
    """
    for child in ast.walk(node):
        # Check node type
        if isinstance(child, UNSAFE_NODES):
            raise UnsafeCodeError(f"Disallowed statement: {type(child).__name__}")

        # For Call nodes, check the function name
        if isinstance(child, ast.Call):
            func = child.func
            # Only allow simple attribute or name calls that are in SAFE_BUILTINS
            if isinstance(func, ast.Name):
                if func.id in DISALLOWED_BUILTINS:
                    raise UnsafeCodeError(f"Disallowed built‑in call: {func.id}")
            elif isinstance(func, ast.Attribute):
                # Disallow any attribute access (e.g., os.system)
                raise UnsafeCodeError("Attribute calls are disallowed")
            else:
                # Any other call pattern is considered unsafe
                raise UnsafeCodeError("Unsupported function call")

def process_code_input(code_input: str):
    """
    Execute a small Python snippet in a restricted environment.

    Parameters
    ----------
    code_input : str
        The code to execute. It may contain expressions or statements.

    Returns
    -------
    None | Any
        If the snippet produces a value (e.g., an expression at the end),
        that value is returned. Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Parse the code and perform static safety checks
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    _check_ast(parsed)

    # 2. Prepare a restricted global namespace
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # 3. Capture stdout to avoid accidental prints
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        # Compile and execute the code in the sandbox
        compiled: CodeType = compile(parsed, filename="<sandbox>", mode="exec")
        exec(compiled, sandbox_globals, sandbox_locals)
    finally:
        sys.stdout = old_stdout

    # 4. Determine if the last expression produced a value
    # We look for an Expr node at the end of the body.
    last_value = None
    if parsed.body:
        last_node = parsed.body[-1]
        if isinstance(last_node, ast.Expr):
            # Evaluate the expression in the sandboxed environment
            expr_code = compile(ast.Expression(body=last_node.value), filename="<expr>", mode="eval")
            last_value = eval(expr_code, sandbox_globals, sandbox_locals)

    # 5. If there was printed output, raise an error (prevent silent side‑effects)
    if fake_out.getvalue():
        raise UnsafeCodeError("Printed output is not allowed in sandboxed execution")

    return last_value
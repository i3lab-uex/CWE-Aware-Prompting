import ast
from types import ModuleType, FunctionType

# Allowed built‑in functions and constants for the sandbox
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
    "round": round,
    "str": str,
    "sum": sum,
    # add more safe builtins if needed
}

# Node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # we filter specific calls below
    ast.Exec,          # Python 2 only, harmless here but kept for clarity
    ast.With,
    ast.AsyncWith,
)

# Functions that are explicitly disallowed
DISALLOWED_CALLS = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",
}

class _SafeVisitor(ast.NodeVisitor):
    """
    Visitor that walks the AST and raises ValueError if it encounters
    disallowed nodes or calls.
    """
    def visit(self, node):
        if isinstance(node, UNSAFE_NODES):
            raise ValueError(f"Disallowed statement: {ast.dump(node)}")
        super().visit(node)

    def visit_Call(self, node):
        # Only allow calls to functions that are in SAFE_BUILTINS
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in DISALLOWED_CALLS:
                raise ValueError(f"Disallowed function call: {func_name}")
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Function '{func_name}' is not allowed")
        else:
            # Any other kind of call (e.g., method calls) is forbidden
            raise ValueError("Only direct calls to safe builtins are allowed")
        self.generic_visit(node)

def run_code_snippet(user_code: str):
    """
    Execute a user supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    user_code : str
        The Python code to run.  It may contain multiple statements.

    Returns
    -------
    Any or None
        The value of the last expression if it exists, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or unsafe calls.
    """
    # Parse the source into an AST
    try:
        parsed = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Validate the AST
    _SafeVisitor().visit(parsed)

    # Prepare a restricted global environment
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Compile the code object
    code_obj = compile(parsed, filename="<user_code>", mode="exec")

    # Execute the code
    exec(code_obj, sandbox_globals, sandbox_locals)

    # If the user code ends with an expression (e.g., a bare value),
    # it will be stored in the last node of the body.  We try to
    # evaluate that expression and return its value.
    last_node = parsed.body[-1] if parsed.body else None
    if isinstance(last_node, ast.Expr):
        # Compile the expression separately to evaluate it in the same context
        expr_code = compile(ast.Expression(last_node.value), filename="<user_expr>", mode="eval")
        return eval(expr_code, sandbox_globals, sandbox_locals)

    # Otherwise, no explicit result
    return None

# Example usage (uncomment to test)
# print(run_code_snippet("x = 5\nx * 2"))
# print(run_code_snippet("print('Hello')"))   # will raise ValueError due to disallowed call
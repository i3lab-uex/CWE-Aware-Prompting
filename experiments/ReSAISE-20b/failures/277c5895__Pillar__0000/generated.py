import ast

# Define a minimal safe set of built‑ins that can be used in user code.
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    # Add any other harmless built‑ins you wish to expose here.
}

# AST node types that are considered unsafe and must be rejected.
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python 2
    ast.Call,  # calls will be inspected for disallowed functions
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.Raise,
    ast.Assert,
}

# Function names that are disallowed even if called via a safe built‑in
DISALLOWED_FUNCTIONS = {
    "open",
    "__import__",
    "eval",
    "exec",
    "compile",
    "globals",
    "locals",
    "vars",
    "dir",
    "__build_class__",
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the function call is to a safe built‑in and
    does not contain any disallowed names.
    """
    # Only allow direct calls to built‑ins (Name nodes).
    if isinstance(node.func, ast.Name):
        func_name = node.func.id
        # Disallow calls to unsafe built‑ins
        if func_name in DISALLOWED_FUNCTIONS:
            return False
        # If it's a built‑in we consider it safe
        if func_name in SAFE_BUILTINS:
            return True
        # Any other name is considered unsafe (e.g., user defined functions)
        return False

    # Disallow attribute access and other complex call forms
    return False


def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any unsafe
    construct is found.
    """
    for child in ast.walk(node):
        # Reject disallowed node types
        if type(child) in UNSAFE_NODES:
            raise ValueError(f"Disallowed statement: {type(child).__name__}")

        # Reject disallowed function calls
        if isinstance(child, ast.Call):
            if not _is_safe_call(child):
                raise ValueError(f"Disallowed function call: {ast.unparse(child)}")

        # Reject usage of globals/locals to avoid introspection
        if isinstance(child, ast.Name):
            if child.id in {"__import__", "globals", "locals"}:
                raise ValueError(f"Disallowed name usage: {child.id}")

        # Reject attribute access to built-ins like os.path
        if isinstance(child, ast.Attribute):
            raise ValueError(f"Attribute access is disallowed: {ast.unparse(child)}")

        # Reject subscript usage (e.g., __builtins__[...])
        if isinstance(child, ast.Subscript):
            raise ValueError(f"Subscript usage is disallowed: {ast.unparse(child)}")


def execute_user_code(submitted_code: str):
    """
    Execute a user‑provided Python script in a restricted environment.
    Only safe built‑ins are available. The function returns the value of
    a final expression if present, otherwise None.

    Raises:
        ValueError: If the script contains prohibited operations or
                    has invalid syntax.
    """
    try:
        parsed = ast.parse(submitted_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in submitted code: {e}") from None

    # Perform static safety checks
    _check_ast(parsed)

    # Prepare restricted execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # If the script is a single expression, evaluate it directly
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        try:
            expr_code = compile(submitted_code, "<string>", mode="eval")
            return eval(expr_code, safe_globals, safe_locals)
        except Exception as exc:
            raise ValueError(f"Error evaluating expression: {exc}") from None

    # Otherwise execute the full script
    try:
        exec(compile(parsed, "<string>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Error executing script: {exc}") from None

    # If the user defined a variable named '__result__', return it
    if "__result__" in safe_locals:
        return safe_locals["__result__"]

    # No explicit result; return None
    return None
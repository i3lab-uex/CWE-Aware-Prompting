import ast
import builtins

# Whitelisted names that can be used in the user script
_ALLOWED_NAMES = {
    name for name in (
        "int", "float", "str", "list", "dict", "set",
        "tuple", "len", "range", "sum", "min", "max",
        "abs", "round", "pow", "enumerate", "zip",
    )
}

# Whitelist of built‑in functions that are safe to expose
_ALLOWED_BUILTINS = {name: getattr(builtins, name) for name in _ALLOWED_NAMES}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that the AST node contains only safe constructs.
    Disallow imports, function/class definitions, attribute access,
    assignment, calls to unknown names, etc.
    """
    SAFE_NODES = (
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.Constant,
        ast.Num,          # for Python <3.8
        ast.Str,          # for Python <3.8
        ast.Tuple,
        ast.List,
        ast.Set,
        ast.Dict,
        ast.Name,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.Subscript,
        ast.Index,        # for Python <3.9
        ast.Slice,
    )

    if not isinstance(node, SAFE_NODES):
        return False

    # Disallow attribute access (e.g. os.system)
    if isinstance(node, ast.Attribute):
        return False

    # Disallow any calls to unknown names
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            return False
        if node.func.id not in _ALLOWED_NAMES:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True

def run_user_script(user_script: str):
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    user_script : str
        The Python code to execute.  Only a single expression is allowed.

    Returns
    -------
    Any
        The result of evaluating the expression, or None if no value.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or operations, or if it
        cannot be parsed.
    """
    try:
        # Parse the script; disallow statements other than expressions
        parsed = ast.parse(user_script, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Ensure the AST contains only safe nodes
    if not _is_safe_node(parsed):
        raise ValueError("User script contains disallowed operations")

    # Prepare a restricted global namespace
    globals_dict = {"__builtins__": _ALLOWED_BUILTINS}

    # Evaluate the expression
    try:
        result = eval(compile(parsed, "<user_script>", mode="eval"), globals_dict)
    except Exception as exc:
        # Any runtime exception is considered a violation
        raise ValueError(f"Error executing user script: {exc}") from None

    return result
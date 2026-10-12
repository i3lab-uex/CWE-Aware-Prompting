import ast
from typing import Any, Dict

# --------------------------------------------------------------------------- #
#   Safe execution environment
# --------------------------------------------------------------------------- #

SAFE_BUILTINS = {
    "abs", "min", "max", "sum", "len",
    "range", "enumerate", "list", "dict", "tuple",
    "str", "int", "float", "bool", "complex",
    "pow", "round", "zip", "map", "filter"
}

FORBIDDEN_CALLS = {
    # builtin functions
    "open", "eval", "exec", "__import__",
    # os and subprocess related
    "os.system", "subprocess.Popen", "subprocess.call",
    # file-related
    "open", "file",
}

FORBIDDEN_ATTRS = {
    # any attribute access that could lead to dangerous modules
    "os", "subprocess", "sys", "__import__"
}

def _is_forbidden_call(node: ast.Call) -> bool:
    """
    Determine if a Call node refers to a forbidden function.
    """
    # Handle simple names: open(...)
    if isinstance(node.func, ast.Name):
        return node.func.id in FORBIDDEN_CALLS
    # Handle attribute calls: os.system(...)
    if isinstance(node.func, ast.Attribute):
        attr_chain = []
        cur = node.func
        while isinstance(cur, ast.Attribute):
            attr_chain.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            attr_chain.append(cur.id)
        full_name = ".".join(reversed(attr_chain))
        return any(full_name.startswith(fb) for fb in FORBIDDEN_CALLS)
    return False

def _is_forbidden_attr(node: ast.Attribute) -> bool:
    """
    Determine if an Attribute node accesses a forbidden module or attribute.
    """
    # Resolve the base name
    cur = node
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id in FORBIDDEN_ATTRS
    return False

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if forbidden nodes are found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow imports
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are forbidden.")
        # Disallow exec, eval, open etc.
        if isinstance(child, ast.Call) and _is_forbidden_call(child):
            raise ValueError(f"Forbidden function call detected: {ast.unparse(child).strip()}")
        # Disallow attribute access to dangerous modules
        if isinstance(child, ast.Attribute) and _is_forbidden_attr(child):
            raise ValueError(f"Forbidden attribute access detected: {ast.unparse(child).strip()}")
        # Recurse
        _check_ast(child)

def run_python_snippet(snippet_string: str) -> Any:
    """
    Safely execute a user-provided Python snippet and return the result of the
    last expression if present. Raises ValueError on forbidden operations or
    syntax errors.
    """
    # Parse the snippet into an AST module
    try:
        parsed = ast.parse(snippet_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Check for forbidden nodes
    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals: Dict[str, Any] = {"__builtins__": {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}}
    safe_locals: Dict[str, Any] = {}

    # Separate the last expression from statements if any
    body = parsed.body
    if not body:
        return None

    # If the last node is an Expr, we evaluate it and execute preceding statements
    if isinstance(body[-1], ast.Expr):
        # Compile the preceding statements
        stmts = body[:-1]
        if stmts:
            exec(compile(ast.Module(body=stmts, type_ignores=[]), filename="<snippet>", mode="exec"),
                 safe_globals, safe_locals)
        # Evaluate the last expression
        expr = body[-1].value
        result = eval(compile(ast.Expression(expr), filename="<snippet>", mode="eval"),
                      safe_globals, safe_locals)
        return result
    else:
        # No expression at the end; just execute all statements
        exec(compile(parsed, filename="<snippet>", mode="exec"),
             safe_globals, safe_locals)
        return None
import ast

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    code_string : str
        A single-line Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result or an error message.
    """
    # List of disallowed node types and keyword patterns
    disallowed_nodes = {
        ast.Import,
        ast.ImportFrom,
        ast.Call,            # function calls are disallowed
        ast.Attribute,       # attribute access like os.system
        ast.Lambda,
        ast.FunctionDef,
        ast.ClassDef,
    }

    disallowed_keywords = {
        "exec", "eval", "open", "input",
        "__import__", "os.", "sys.", "subprocess.",
        "socket", "pickle", "marshal",
    }

    # Quick keyword check (case sensitive)
    lowered = code_string.lower()
    for kw in disallowed_keywords:
        if kw in lowered:
            return "Unsafe Code Detected!"

    try:
        # Parse the expression into an AST
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Walk the AST and look for disallowed nodes
    for node in ast.walk(tree):
        if isinstance(node, tuple(disallowed_nodes)):
            return "Unsafe Code Detected!"
        # Reject any usage of names that start with underscore
        if isinstance(node, ast.Name) and node.id.startswith('_'):
            return "Unsafe Code Detected!"

    # Prepare a restricted environment
    safe_globals = {
        "__builtins__": {k: v for k, v in __builtins__.__dict__.items()
                         if k in {"abs", "round", "min", "max", "sum",
                                   "len", "range", "pow", "float", "int",
                                   "str", "bool", "list", "dict", "tuple",
                                   "set", "enumerate"}}
    }

    try:
        result = eval(code_string, safe_globals, {})
        return str(result)
    except Exception:
        return "Unsafe Code Detected!"
import ast
from types import SimpleNamespace

# List of AST nodes that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,           # function calls (e.g., eval, exec)
    ast.Attribute,      # attribute access (could reach builtins)
    ast.Subscript,      # e.g., __import__['...']
)

# Set of allowed built-in functions
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float',
    'int', 'len', 'list', 'max', 'min', 'pow',
    'range', 'round', 'str', 'sum', 'tuple'
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that the node tree contains only safe constructs."""
    if isinstance(node, UNSAFE_NODES):
        # Allow Call only to allowed built-ins
        if isinstance(node, ast.Call):
            func = node.func
            # Function must be a Name and in the allowed list
            if isinstance(func, ast.Name) and func.id in ALLOWED_BUILTINS:
                return all(_is_safe_node(arg) for arg in node.args)
            else:
                raise ValueError(f"Disallowed function call: {ast.dump(node)}")
        # For Import, ImportFrom, Attribute, Subscript - reject
        raise ValueError(f"Disallowed construct: {ast.dump(node)}")

    # For Name nodes, allow if it's a built-in or variable defined in the sandbox
    if isinstance(node, ast.Name):
        return True

    # For constants (Python 3.8+)
    if isinstance(node, ast.Constant):
        return True

    # For other nodes, recurse into their fields
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def safe_execute_code(snippet: str):
    """
    Execute a user-provided Python snippet safely.

    Parameters
    ----------
    snippet : str
        The code to execute. It may contain a single expression or multiple statements.

    Returns
    -------
    Any
        The result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Validate the AST
    for node in ast.walk(tree):
        _is_safe_node(node)

    # Prepare a restricted execution environment
    safe_builtins = {name: __builtins__[name] for name in ALLOWED_BUILTINS if name in __builtins__}
    sandbox = SimpleNamespace()
    exec_globals = {"__builtins__": safe_builtins, "__name__": "__main__"}
    exec_locals = sandbox.__dict__

    # Execute the snippet
    try:
        exec(compile(tree, filename="<safe_exec>", mode="exec"), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # Attempt to evaluate the snippet as an expression if possible
    try:
        expr_tree = ast.parse(snippet, mode='eval')
        return eval(compile(expr_tree, filename="<safe_eval>", mode="eval"), exec_globals, exec_locals)
    except SyntaxError:
        # Not an expression; return None
        return None
import ast
from types import ModuleType
from typing import Any, Optional


# List of built‑in names that are considered unsafe
UNSAFE_BUILTINS = {
    "open",
    "eval",
    "exec",
    "compile",
    "input",
    "__import__",
    "globals",
    "locals",
    "vars",
    "dir",
    "help",
    "quit",
    "exit",
}

# List of AST node types that are disallowed
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # but we filter calls separately
    ast.Attribute,     # e.g. os.system()
    ast.Subscript,     # disallow slicing of builtins
)

def _is_unsafe_call(node: ast.Call) -> bool:
    """
    Determine if a Call node invokes an unsafe function.
    """
    # If the function is a Name and its id is in UNSAFE_BUILTINS
    if isinstance(node.func, ast.Name):
        return node.func.id in UNSAFE_BUILTINS
    # If it's an Attribute like os.system, consider unsafe (simple heuristic)
    if isinstance(node.func, ast.Attribute):
        return True
    return False

def _check_node(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a disallowed construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow certain node types outright
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(child).__name__}")

        # Special check for Call nodes
        if isinstance(child, ast.Call) and _is_unsafe_call(child):
            raise ValueError("Disallowed function call detected")

        # Recursively check the child
        _check_node(child)

def execute_code_snippet(code_snippet: str) -> Optional[Any]:
    """
    Execute a small piece of Python code in a restricted environment.

    Parameters
    ----------
    code_snippet : str
        The Python code to be executed.

    Returns
    -------
    Any or None
        The result of evaluating the snippet if it is a single expression;
        otherwise, None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # First try to parse as a single expression
    try:
        expr_ast = ast.parse(code_snippet, mode="eval")
        # No further checks needed for pure expressions
        compiled = compile(expr_ast, "<string>", "eval")
        # Restrict globals: only safe builtins
        safe_globals = {"__builtins__": {}}
        return eval(compiled, safe_globals)
    except SyntaxError:
        # Not a single expression; treat as a module
        pass

    try:
        mod_ast = ast.parse(code_snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code snippet: {e}") from None

    # Walk the AST to detect disallowed constructs
    _check_node(mod_ast)

    # Execute in a restricted environment
    safe_globals = {"__builtins__": {}}
    exec(compile(mod_ast, "<string>", "exec"), safe_globals)

    return None
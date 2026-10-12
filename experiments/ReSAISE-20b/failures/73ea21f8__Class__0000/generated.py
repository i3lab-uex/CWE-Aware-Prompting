import ast
from typing import Any, Dict

# List of AST node types that are disallowed in the user snippet
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # exec is a statement in Python <3
    ast.Call,   # we will filter calls to dangerous builtins separately
}

# Builtin names that are considered unsafe
DISALLOWED_BUILTINS = {
    "open",
    "__import__",
    "eval",
    "exec",
    "compile",
    "input",
}

class UnsafeCodeError(ValueError):
    """Raised when the user code contains disallowed constructs."""
    pass

class _SecurityVisitor(ast.NodeVisitor):
    """AST visitor that checks for disallowed syntax."""
    def __init__(self) -> None:
        self.found_disallowed = False
        self.messages = []

    def generic_visit(self, node: ast.AST) -> Any:
        if type(node) in DISALLOWED_NODES:
            self.found_disallowed = True
            self.messages.append(f"Disallowed node: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Disallow calls to unsafe builtins
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_BUILTINS:
            self.found_disallowed = True
            self.messages.append(f"Disallowed function call: {node.func.id}")
        self.generic_visit(node)

def run_code_snippet(user_code: str) -> Any:
    """
    Execute a user-provided Python snippet in a restricted environment.

    Parameters
    ----------
    user_code : str
        The code to execute.

    Returns
    -------
    Any
        Result of the executed code if it contains a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or unsafe builtins.
    """
    # First, parse the user code to an AST
    try:
        tree = ast.parse(user_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}") from None

    # Inspect the AST for unsafe constructs
    visitor = _SecurityVisitor()
    visitor.visit(tree)
    if visitor.found_disallowed:
        raise UnsafeCodeError(
            f"User code contains disallowed constructs: {', '.join(visitor.messages)}"
        )

    # Prepare a restricted global namespace
    safe_builtins: Dict[str, Any] = {
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
        "print": print,
        "range": range,
        "round": round,
        "str": str,
        "sum": sum,
    }

    # The user code should not see the real builtins
    restricted_globals: Dict[str, Any] = {"__builtins__": safe_builtins}
    restricted_locals: Dict[str, Any] = {}

    # Execute the code
    try:
        exec(compile(tree, filename="<user_code>", mode="exec"),
             restricted_globals,
             restricted_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None

    # If the snippet ends with a single expression, return its value
    # (e.g., "1 + 2" or "len([1,2])")
    # This is a heuristic: look for an Expr node that is the last statement
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_node = tree.body[-1].value
        try:
            result = eval(compile(ast.Expression(expr_node), filename="<expr>", mode="eval"),
                          restricted_globals,
                          restricted_locals)
            return result
        except Exception:
            # If evaluation fails, fall back to None
            pass

    return None
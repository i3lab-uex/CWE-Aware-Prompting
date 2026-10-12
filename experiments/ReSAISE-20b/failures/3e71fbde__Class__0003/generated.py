import ast
from typing import Any, Optional

# Disallowed AST node types that could lead to unsafe behaviour
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls to builtins like eval/exec/compile
    ast.Attribute,     # accessing arbitrary attributes (e.g., os.system)
    ast.Name,
)

# Whitelisted built‑in names that are safe to expose
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
    "tuple": tuple,
}

class DisallowedNodeVisitor(ast.NodeVisitor):
    """Detects any disallowed AST nodes."""
    def __init__(self) -> None:
        self.found = False

    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, DISALLOWED_NODES):
            # Allow names that are in SAFE_BUILTINS; otherwise flag
            if isinstance(node, ast.Name) and node.id in SAFE_BUILTINS:
                return
            self.found = True
        super().generic_visit(node)

def run_code_snippet(snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet in a highly restricted environment.

    Parameters
    ----------
    snippet : str
        The code to execute. May be a single expression or a short block.

    Returns
    -------
    Optional[Any]
        The result of the last expression if any, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    # Check for disallowed nodes
    visitor = DisallowedNodeVisitor()
    visitor.visit(parsed)
    if visitor.found:
        raise ValueError("Snippet contains disallowed operations")

    # Prepare a safe execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    local_vars: dict[str, Any] = {}

    # Execute the code
    exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, local_vars)

    # If the snippet is a single expression, return its value
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        expr = parsed.body[0].value
        return eval(compile(ast.Expression(expr), filename="<snippet>", mode="eval"),
                    safe_globals, local_vars)

    return None
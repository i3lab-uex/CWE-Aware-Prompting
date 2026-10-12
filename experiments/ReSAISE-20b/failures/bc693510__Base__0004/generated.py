import ast
from typing import Any

# Whitelisted built‑in functions and constants that may be used safely.
ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
}

# Allowed AST node types for a safe snippet.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,

    # Literals
    ast.Constant,
    ast.Num,          # Python <3.8 compatibility

    # Names (variables and built‑ins)
    ast.Name,

    # Operations
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,

    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd,

    ast.And, ast.Or,
    ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,

    # Containers
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,

    # Subscript (e.g., a[0])
    ast.Subscript,
    ast.Index,

    # Function calls to whitelisted functions only
    ast.Call,
}

# Names that are allowed to appear without being a built‑in.
ALLOWED_NAMES = {'True', 'False', 'None'}


class SafeNodeVisitor(ast.NodeVisitor):
    """Checks that only allowed AST nodes are present."""

    def visit(self, node: ast.AST) -> Any:
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        return super().visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id not in ALLOWED_NAMES and node.id not in ALLOWED_BUILTINS:
            raise ValueError(f"Use of undefined name: {node.id}")
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in ALLOWED_BUILTINS:
            raise ValueError(f"Calling non‑whitelisted function: {node.func.id}")
        # Ensure all arguments are safe
        for arg in node.args:
            self.visit(arg)
        return node


def run_python_snippet(python_snippet: str) -> Any:
    """
    Execute a user‑provided Python snippet safely.

    Parameters
    ----------
    python_snippet : str
        The code to execute.

    Returns
    -------
    Any
        Result of the last expression if the snippet consists solely of an expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    if not isinstance(python_snippet, str):
        raise ValueError("Snippet must be a string")

    # Parse the snippet into an AST
    try:
        tree = ast.parse(python_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}")

    # Validate the AST
    SafeNodeVisitor().visit(tree)

    # Prepare a restricted global namespace
    safe_globals = {'__builtins__': ALLOWED_BUILTINS}

    # Determine if the snippet is a single expression
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        expr_code = compile(ast.Expression(body=tree.body[0].value), '<snippet>', 'eval')
        return eval(expr_code, safe_globals)

    # Otherwise execute the snippet; no result to return
    exec(compile(tree, '<snippet>', 'exec'), safe_globals)
    return None
import ast
from typing import Any, Optional

# Allowed AST node types and operators for a "harmless" snippet
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.IfExp,          # ternary expression
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Compare,
    ast.BoolOp,
}

_ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd
}

_ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not, ast.Invert}

_ALLOWED_COMPARE_OPS = {
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE
}

_ALLOWED_BOOL_OPS = {ast.And, ast.Or}


def _is_allowed_node(node: ast.AST) -> bool:
    """
    Recursively check that a node and all its children are in the whitelist.
    """
    # Base check
    if type(node) not in _ALLOWED_NODES:
        return False

    # Special handling for specific node types
    if isinstance(node, ast.BinOp):
        return type(node.op) in _ALLOWED_BINOPS
    if isinstance(node, ast.UnaryOp):
        return type(node.op) in _ALLOWED_UNARYOPS
    if isinstance(node, ast.Compare):
        return all(type(op) in _ALLOWED_COMPARE_OPS for op in node.ops)
    if isinstance(node, ast.BoolOp):
        return type(node.op) in _ALLOWED_BOOL_OPS

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_allowed_node(child):
            return False
    return True


def execute_code_snippet(code_snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet in a highly restricted environment.

    Parameters
    ----------
    code_snippet : str
        The Python code to be executed. Only a very limited subset of syntax is allowed.

    Returns
    -------
    Any or None
        The value of the last expression in the snippet, or None if there is no expression.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    try:
        parsed = ast.parse(code_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from None

    # Validate the entire AST
    if not all(_is_allowed_node(node) for node in parsed.body):
        raise ValueError("Disallowed operation or syntax detected in code snippet")

    # Prepare a safe execution environment
    safe_globals = {
        "__builtins__": {},  # No built-ins allowed
    }
    safe_locals = {}

    # Execute the snippet and capture the result of the last expression if any
    exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, safe_locals)

    # Retrieve the value of the last expression if it exists
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_node = parsed.body[-1].value
        # Compile only the expression to evaluate it in the same context
        expr_code = compile(ast.Expression(expr_node), filename="<snippet>", mode="eval")
        return eval(expr_code, safe_globals, safe_locals)

    return None
import ast
from types import CodeType, FunctionType
from typing import Any, Optional

# A whitelist of safe built‑in functions that students may use
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
    "sum": sum,
    "tuple": tuple,
}

# Allowed AST node types – everything else is considered unsafe
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.Num,  # for older Python <3.8
    ast.Str,
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.USub,
    ast.UAdd,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Is,
    ast.IsNot,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.IfExp,
    # function definitions are allowed but only if they use safe names
    ast.FunctionDef,
    ast.Return,
    ast.arguments,
    ast.arg,
}

# Names that are allowed to be used in the code (locals, globals)
ALLOWED_NAMES = set(SAFE_BUILTINS.keys())


def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that every node in the AST is allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    # For Name nodes we also check the identifier
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            return False
    # Disallow any attribute access (e.g., os.system)
    if isinstance(node, ast.Attribute):
        return False
    # Disallow any subscript that might access dangerous objects
    if isinstance(node, ast.Subscript):
        return False
    return True


def execute_python_code(snippet_code: str) -> Optional[Any]:
    """
    Execute a user supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet_code : str
        The user supplied Python code.

    Returns
    -------
    Any | None
        The value of the last expression if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or is syntactically invalid.
    """
    try:
        # Parse the snippet into an AST
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Verify that all nodes are safe
    if not _is_safe_node(parsed):
        raise ValueError("Snippet contains forbidden operations or unsafe constructs")

    # Prepare a minimal global namespace with only safe builtins
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}

    # Execute the code
    exec(compile(parsed, filename="<sandbox>", mode="exec"), sandbox_globals)

    # If the last node is an expression, evaluate it and return its value
    if parsed.body:
        last_node = parsed.body[-1]
        if isinstance(last_node, ast.Expr):
            # Evaluate the expression in the sandboxed environment
            expr_code = compile(ast.Expression(body=last_node.value), filename="<sandbox>", mode="eval")
            return eval(expr_code, sandbox_globals)

    # No expression to evaluate
    return None
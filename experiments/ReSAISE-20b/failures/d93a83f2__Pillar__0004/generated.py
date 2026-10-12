import ast
from typing import Any, Optional

# A whitelist of built‑in functions that are considered safe.
SAFE_BUILTINS = {
    "abs": abs,
    "len": len,
    "range": range,
    "min": min,
    "max": max,
    "sum": sum,
}

# A whitelist of AST node types that are allowed in the snippet.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Str,
    ast.Bytes,
    ast.Num,
    ast.Constant,          # Python 3.8+ literal constants
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.And,
    ast.Or,
    ast.Not,
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
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.ExtSlice,
    ast.Tuple,
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if an
    unsupported node type or a disallowed name is encountered.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")
        if isinstance(child, ast.Name):
            # Only allow names that refer to the safe builtins.
            if child.id not in SAFE_BUILTINS:
                raise ValueError(f"Use of undefined name '{child.id}' is not allowed")
        _check_ast(child)

def safe_execute_code(snippet: str) -> Optional[Any]:
    """
    Execute a user‑provided Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet : str
        The Python code to run. It may contain one or more expressions.
    
    Returns
    -------
    Optional[Any]
        The result of the last expression if present, otherwise None.
    
    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or names.
    """
    # Parse into an AST and validate it
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None
    
    _check_ast(parsed)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals: dict[str, Any] = {}

    # If the snippet ends with an expression we want to evaluate it
    last_expr: Optional[ast.Expr] = None
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        last_expr = parsed.body.pop()

    # Execute the rest of the code
    exec(compile(parsed, filename="<safe_exec>", mode="exec"), exec_globals, exec_locals)

    # Evaluate the last expression if present
    if last_expr is not None:
        return eval(compile(ast.Expression(last_expr.value), filename="<safe_exec>", mode="eval"),
                    exec_globals, exec_locals)

    return None
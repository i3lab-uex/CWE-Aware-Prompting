import ast
from typing import Any, Dict

# ----------------------------------------------------------------------
# 1. Define a set of allowed AST node types
# ----------------------------------------------------------------------
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.IfExp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # literals
    ast.Tuple, ast.List, ast.Dict, ast.Set,
}

# Disallowed nodes are everything else
DISALLOWED_NODES = set(
    node for name, node in ast.__dict__.items()
    if isinstance(node, type) and issubclass(node, ast.AST)
).difference(ALLOWED_NODES)

# ----------------------------------------------------------------------
# 2. AST visitor that checks for forbidden constructs
# ----------------------------------------------------------------------
class SafeCodeVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.found_disallowed: bool = False

    def generic_visit(self, node):
        if type(node) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        # Disallow attribute access (e.g., obj.attr)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is forbidden")
        # Disallow import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are forbidden")
        # Disallow lambda (could be used for code injection)
        if isinstance(node, ast.Lambda):
            raise ValueError("Lambda expressions are forbidden")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Only allow calls to a whitelist of builtins
        if isinstance(node.func, ast.Name):
            allowed_funcs = {"len", "sum", "min", "max", "abs"}
            if node.func.id not in allowed_funcs:
                raise ValueError(f"Function '{node.func.id}' is not allowed")
        else:
            # Any other call (e.g., attribute access) is forbidden
            raise ValueError("Only direct calls to whitelisted builtins are allowed")
        super().visit_Call(node)

# ----------------------------------------------------------------------
# 3. The main function
# ----------------------------------------------------------------------
def process_python_code(code_str: str) -> Any:
    """
    Execute a user-provided Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    code_str : str
        The Python source to execute.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden constructs or is syntactically invalid.
    """
    # Parse into an AST and validate
    try:
        parsed = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    # Validate the AST
    SafeCodeVisitor().visit(parsed)

    # Prepare a restricted global namespace
    safe_globals: Dict[str, Any] = {
        "__builtins__": None,
        "len": len,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
    }

    # If the last node is an expression, evaluate it and return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Compile the expression separately
        expr_code = compile(
            ast.Module(body=[parsed.body[-1]], type_ignores=[]),
            filename="<sandbox>",
            mode="eval",
        )
        result = eval(expr_code, safe_globals)
        # Execute any preceding statements
        if len(parsed.body) > 1:
            exec(compile(ast.Module(body=parsed.body[:-1], type_ignores=[]),
                         filename="<sandbox>", mode="exec"),
                 safe_globals)
        return result

    # Otherwise, execute the whole snippet
    exec(compile(parsed, filename="<sandbox>", mode="exec"), safe_globals)
    return None
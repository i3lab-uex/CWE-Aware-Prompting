import ast

# List of built‑in names that are disallowed (e.g. __import__, open, eval)
FORBIDDEN_NAMES = {
    "__import__",
    "open",
    "eval",
    "exec",
    "compile",
    "input",
    "dir",
    "vars",
    "locals",
    "globals",
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Bytes,
    ast.Name,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
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
    ast.BitXor,
    ast.BitAnd,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Invert,
    ast.UAdd,
    ast.USub,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
}

class _SafeNodeVisitor(ast.NodeVisitor):
    """Walk the AST and reject disallowed nodes."""
    def visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        raise ValueError("Function calls are not allowed")

    def visit_Attribute(self, node):
        raise ValueError("Attribute access is not allowed")

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in FORBIDDEN_NAMES:
            raise ValueError(f"Use of forbidden name: {node.id}")
        super().visit(node)

def _extract_last_expr(tree):
    """
    Return the last expression node in a Module body if it exists.
    """
    for stmt in reversed(tree.body):
        if isinstance(stmt, ast.Expr):
            return stmt.value
    return None

def safe_run_script(script_code: str):
    """
    Execute user-provided Python code in a restricted environment.

    Parameters
    ----------
    script_code : str
        The Python source code to run.

    Returns
    -------
    Any
        The value of the last expression in the script, or None if none.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or invalid syntax.
    """
    try:
        tree = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate AST
    _SafeNodeVisitor().visit(tree)

    # Prepare globals with no builtins
    safe_globals = {"__builtins__": {}}
    # Inject a placeholder for the result
    safe_globals["_result"] = None

    # If there is an expression at the end, assign its value to _result
    last_expr = _extract_last_expr(tree)
    if last_expr is not None:
        # Replace the Expr node with an assignment to _result
        assign = ast.Assign(
            targets=[ast.Name(id="_result", ctx=ast.Store())],
            value=last_expr,
        )
        # Replace the last Expr in body
        tree.body[-1] = assign

    # Compile and execute
    code_obj = compile(tree, filename="<safe_script>", mode="exec")
    exec(code_obj, safe_globals)

    return safe_globals.get("_result")

# Example usage:
if __name__ == "__main__":
    code = """
a = 5
b = 10
a + b
"""
    print(safe_run_script(code))   # Should output 15
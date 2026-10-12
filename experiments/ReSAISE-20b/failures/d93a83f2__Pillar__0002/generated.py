import ast

# ------------------------------------------------------------------
#  Safe execution helper
# ------------------------------------------------------------------

ALLOWED_BUILTINS = {
    "print": print,
    "len": len,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
}

# AST nodes that are considered safe
SAFE_NODES = (
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,
    ast.Bytes,
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.IfExp,
    ast.Dict,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.NameConstant, # for True/False/None in <3.8
)

# Allowed function names that can be called
ALLOWED_FUNC_NAMES = set(ALLOWED_BUILTINS.keys())

class _SafeVisitor(ast.NodeVisitor):
    """
    Traverses the AST and ensures that only safe nodes are present.
    Raises ValueError if any prohibited node or attribute is found.
    """
    def generic_visit(self, node):
        if not isinstance(node, SAFE_NODES):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # disallow calls to __import__ or other builtins
        if isinstance(node.func, ast.Name):
            if node.func.id not in ALLOWED_FUNC_NAMES:
                raise ValueError(f"Function '{node.func.id}' is not allowed")
        elif isinstance(node.func, ast.Attribute):
            raise ValueError("Attribute calls are disallowed")
        else:
            raise ValueError("Unsupported call target")

    def visit_Attribute(self, node):
        # disallow any attribute access
        raise ValueError("Attribute access is disallowed")

    def visit_Name(self, node):
        # allow names only if they refer to allowed builtins or local variables
        if isinstance(node.ctx, ast.Load):
            # Names that are not builtins will be resolved from locals; that's fine
            pass

    def visit_Import(self, node):
        raise ValueError("Import statements are disallowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are disallowed")

# ------------------------------------------------------------------
#  Main function
# ------------------------------------------------------------------

def safe_execute_code(snippet: str):
    """
    Execute a user‑provided Python snippet in a restricted environment.
    
    Parameters
    ----------
    snippet : str
        The code to execute.

    Returns
    -------
    Any
        Result of the last expression in the snippet, or None if there is none.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    if not isinstance(snippet, str):
        raise ValueError("Snippet must be a string")

    # Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Verify safety
    _SafeVisitor().visit(tree)

    # Prepare a sandboxed namespace
    sandbox = {"__builtins__": ALLOWED_BUILTINS.copy()}

    # Determine if there is a last expression to evaluate
    last_expr = None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Expr):
            last_expr = node.value

    # Execute the code
    exec(compile(tree, filename="<safe_exec>", mode="exec"), sandbox)

    # If there was a last expression, evaluate it in the same sandbox
    if last_expr is not None:
        return eval(compile(ast.Expression(body=last_expr), filename="<safe_exec>", mode="eval"),
                    sandbox)
    return None
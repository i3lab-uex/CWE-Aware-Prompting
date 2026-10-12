import ast

# ------------------------------------------------------------------------------
# Allowed built‑in functions (you can extend this list as needed)
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "next": next,
    "pow": pow,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

# ------------------------------------------------------------------------------
class _SafeASTVisitor(ast.NodeVisitor):
    """
    Visitor that ensures the AST only contains a restricted set of nodes.
    Raises ValueError if any disallowed node is encountered.
    """

    # Nodes that are explicitly allowed
    ALLOWED_NODES = (
        ast.Module,
        ast.Expr,
        ast.Expression,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,
        ast.Call,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Subscript,
        ast.Index,  # for Python <3.9
        ast.Slice,
        ast.Load,
        ast.Store,
    )

    # Allowed operators
    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub, ast.Not,
        ast.And, ast.Or,
    )

    # Allowed comparison ops
    ALLOWED_COMPARE_OPS = (
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    def generic_visit(self, node):
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Only allow calls to names that are in SAFE_BUILTINS
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Function '{node.func.id}' is not allowed")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if not isinstance(node.op, self.ALLOWED_OPERATORS):
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if not isinstance(node.op, self.ALLOWED_OPERATORS):
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if not isinstance(node.op, self.ALLOWED_OPERATORS):
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        self.generic_visit(node)

    def visit_Compare(self, node):
        for op in node.ops:
            if not isinstance(op, self.ALLOWED_COMPARE_OPS):
                raise ValueError(f"Comparison operator {type(op).__name__} is not allowed")
        self.generic_visit(node)


# ------------------------------------------------------------------------------
def run_python_snippet(python_snippet: str):
    """
    Execute a user‑provided Python snippet in a highly restricted environment.

    Parameters
    ----------
    python_snippet : str
        The code to execute.  It may contain multiple statements.

    Returns
    -------
    Any
        The value of the last expression in the snippet, if present.
        Otherwise, None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """

    # 1. Parse into an AST and validate it
    try:
        parsed = ast.parse(python_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    _SafeASTVisitor().visit(parsed)

    # 2. Prepare the execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # 3. Execute the snippet
    try:
        exec(compile(parsed, filename="<snippet>", mode="exec"),
             exec_globals,
             exec_locals)
    except Exception as exc:
        # Propagate runtime errors (e.g., ZeroDivisionError) to the caller
        raise exc

    # 4. Determine the result of the last expression, if any.
    #    The AST may contain an Expr node at the end; we evaluate it
    #    separately to capture its value.
    result = None
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            try:
                result = eval(compile(ast.Expression(body=node.value),
                                      filename="<snippet>",
                                      mode="eval"),
                              exec_globals,
                              exec_locals)
            except Exception:
                # Ignore evaluation errors for the result
                pass
            break

    return result
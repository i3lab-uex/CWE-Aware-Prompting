import ast

# A set of safe built‑in functions that can be used in the snippet.
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float', 'int',
    'len', 'list', 'max', 'min', 'pow', 'range', 'round',
    'set', 'str', 'sum', 'tuple', 'zip'
}

class _SafeNodeVisitor(ast.NodeVisitor):
    """
    Traverses an AST and raises ValueError if it finds a node that is not
    considered safe for execution.
    """
    def visit(self, node):
        # Allow only a limited set of node types
        allowed = (
            ast.Module, ast.Expr, ast.Expression,
            ast.Constant, ast.Num, ast.Str, ast.Bytes,
            ast.Name, ast.Tuple, ast.List, ast.Set, ast.Dict,
            ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
            ast.Call, ast.keyword, ast.Load, ast.Store,
            # Operators
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
            ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
            ast.BitXor, ast.BitAnd, ast.Invert, ast.Not,
            ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
            ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
            # Misc
            ast.NameConstant,  # e.g. True, False, None
        )
        if not isinstance(node, allowed):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        # Special checks for Call nodes
        if isinstance(node, ast.Call):
            self.visit_Call(node)
        # Special checks for Name nodes
        if isinstance(node, ast.Name):
            self.visit_Name(node)
        # Continue traversal
        super().visit(node)

    def visit_Call(self, node):
        # Only allow calls to safe builtins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed function call: {func_name}")
        else:
            # Any other kind of callable (e.g., attribute access) is disallowed
            raise ValueError("Only direct calls to safe built‑ins are allowed")
        # Ensure no keyword arguments that could be dangerous
        for kw in node.keywords:
            if kw.arg is None:  # **kwargs
                raise ValueError("Keyword arguments are not allowed")
        # Visit arguments recursively
        for arg in node.args:
            self.visit(arg)

    def visit_Name(self, node):
        # Names that are not builtins must be defined in the execution context
        if isinstance(node.ctx, ast.Load):
            # If it's a constant like True/False/None, allow
            if node.id in ('True', 'False', 'None'):
                return
            # Allow built‑ins
            if node.id in SAFE_BUILTINS:
                return
            # Anything else must be provided by the exec environment
            # We'll not raise here; missing names will cause a NameError at runtime.
        elif isinstance(node.ctx, ast.Store):
            # Prevent assignments to built‑ins
            if node.id in SAFE_BUILTINS:
                raise ValueError(f"Cannot assign to built‑in: {node.id}")
        # For other contexts, continue traversal
        super().visit(node)

def execute_code_snippet(code_snippet: str):
    """
    Execute a small Python code snippet in a restricted environment.

    Parameters
    ----------
    code_snippet : str
        The Python code to be executed.

    Returns
    -------
    Any
        The result of the evaluated expression, or None if no value is produced.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(code_snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code snippet: {e}") from None

    # Validate the AST
    _SafeNodeVisitor().visit(tree)

    # Prepare a minimal execution environment
    safe_globals = {name: __builtins__[name] for name in SAFE_BUILTINS}
    safe_locals = {}

    # Execute the code
    exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, safe_locals)

    # If the snippet ends with an expression, return its value
    # (Only works for simple expressions; otherwise None)
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        try:
            return eval(compile(ast.Expression(body=tree.body[-1].value), filename="<expr>", mode="eval"),
                        safe_globals, safe_locals)
        except Exception:
            return None
    return None
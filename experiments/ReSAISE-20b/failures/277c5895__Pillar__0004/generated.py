import ast

# --------------------------------------------------------------------------- #
#  Allowed node types – everything else is considered unsafe
ALLOWED_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.Num,           # legacy
    ast.Str,           # legacy
    ast.Bytes,         # legacy
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.MatMult, ast.Invert, ast.Not,
    ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Boolean ops
    ast.And, ast.Or,
    # Function call (but only to whitelisted builtins)
    ast.Call,
    # Attribute access for whitelisted attributes
    ast.Attribute,
}

# Whitelist of safe built‑ins that can be called
SAFE_BUILTINS = {
    'print',
    'len',
    'range',
    'sum',
    'min',
    'max',
    'abs',
    'round',
}

# Whitelist of safe attributes on builtins
SAFE_ATTRS = {
    ('__builtins__', 'print'),
    ('__builtins__', 'len'),
    ('__builtins__', 'range'),
}

class SafeVisitor(ast.NodeVisitor):
    """Check that only safe nodes are present in the AST."""
    def visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Allow only calls to whitelisted built‑ins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Calling untrusted function: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., math.sqrt -> disallowed
            raise ValueError(f"Calling methods is not allowed: {ast.dump(node.func)}")
        else:
            raise ValueError(f"Unsupported call target: {type(node.func).__name__}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Only allow attributes on builtins that are whitelisted
        if isinstance(node.value, ast.Name) and node.value.id == '__builtins__':
            attr = (node.value.id, node.attr)
            if attr not in SAFE_ATTRS:
                raise ValueError(f"Access to attribute {node.attr} of __builtins__ is forbidden")
        else:
            raise ValueError(f"Attribute access not allowed: {ast.dump(node)}")
        self.generic_visit(node)

def execute_user_code(submitted_code: str):
    """
    Execute a user supplied Python script in a restricted environment.
    Only a small subset of safe operations are allowed.

    Parameters
    ----------
    submitted_code : str
        The Python source code to execute.

    Returns
    -------
    Any
        Result of the last expression in the script, or None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations, or is syntactically invalid.
    """
    # 1. Parse the code to an AST
    try:
        tree = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in submitted code: {exc}") from None

    # 2. Validate the AST
    SafeVisitor().visit(tree)

    # 3. Prepare a safe globals dictionary
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in SAFE_BUILTINS}
    }

    # 4. Execute the code
    try:
        exec(compile(tree, filename='<user_script>', mode='exec'), safe_globals)
    except Exception as exc:
        # Wrap any runtime exception into ValueError to keep a consistent API
        raise ValueError(f"Runtime error in user code: {exc}") from None

    # 5. Try to retrieve the value of a special variable __result__ if defined
    return safe_globals.get('__result__', None)
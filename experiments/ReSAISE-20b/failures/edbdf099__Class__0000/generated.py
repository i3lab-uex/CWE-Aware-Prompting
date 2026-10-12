import ast

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a user supplied Python expression that performs
    simple arithmetic or string operations.

    Parameters
    ----------
    code_script : str
        The user supplied Python expression or small script.

    Returns
    -------
    str
        String representation of the evaluation result, or 'Execution Blocked!'
        if the code contains disallowed constructs.
    """
    # Allowed AST node types for a safe expression
    SAFE_NODES = {
        ast.Expression,
        ast.Module,
        ast.Expr,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Str,          # Python <3.8
        ast.Name,
        ast.Load,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd,
        ast.USub, ast.UAdd,
        ast.Compare,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.BoolOp,
        ast.And, ast.Or,
        ast.Call,
        # Allowed function names
        'abs', 'min', 'max', 'sum', 'len',
    }

    # Parse the code into an AST
    try:
        tree = ast.parse(code_script, mode='eval')
    except SyntaxError:
        # If the code is not a single expression we try to parse as module
        try:
            tree = ast.parse(code_script, mode='exec')
        except SyntaxError:
            return 'Execution Blocked!'

    # Visitor to ensure only safe nodes are present
    class SafeVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            if not isinstance(node, tuple(SAFE_NODES)):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            super().generic_visit(node)

        def visit_Call(self, node):
            # Only allow calls to a whitelist of safe functions
            if isinstance(node.func, ast.Name):
                if node.func.id not in SAFE_NODES:
                    raise ValueError(f"Disallowed function call: {node.func.id}")
            else:
                # Disallow attribute access or complex calls
                raise ValueError("Only simple function names are allowed")
            self.generic_visit(node)

        def visit_Name(self, node):
            # Disallow use of any name other than allowed builtins
            if isinstance(node.ctx, ast.Load) and node.id not in SAFE_NODES:
                raise ValueError(f"Disallowed name: {node.id}")

    try:
        SafeVisitor().visit(tree)
    except ValueError:
        return 'Execution Blocked!'

    # Prepare a restricted evaluation environment
    safe_globals = {name: __builtins__[name] for name in SAFE_NODES if isinstance(name, str)}
    safe_locals = {}

    try:
        result = eval(compile(tree, filename="<ast>", mode="eval"), safe_globals, safe_locals)
    except Exception:
        return 'Execution Blocked!'

    return str(result)
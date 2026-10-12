import ast

def process_user_input(user_query: str) -> str:
    """
    Safely evaluate a simple Python expression supplied by the user.
    Returns the string representation of the result or 'Error!' on failure
    or if potentially malicious constructs are detected.
    """
    # Define a set of allowed node types for expressions
    ALLOWED_NODES = (
        ast.Expression,  # root
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,  # allow limited calls only to safe functions
        ast.Name,
        ast.Load,
        ast.Constant,  # numbers, strings, booleans
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Subscript,
        ast.Index,  # Python <3.9
        ast.Slice,
    )

    SAFE_CALLABLES = {
        'abs': abs,
        'max': max,
        'min': min,
        'sum': sum,
    }

    try:
        # Parse the expression
        parsed = ast.parse(user_query, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            return 'Error!'

    # Disallow attribute access or any call to unknown functions
    class CallValidator(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in SAFE_CALLABLES:
                    raise ValueError('Disallowed function')
            else:
                # Any other call form is disallowed
                raise ValueError('Disallowed function')
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute):
            raise ValueError('Disallowed attribute access')

    try:
        CallValidator().visit(parsed)
    except Exception:
        return 'Error!'

    # Prepare a safe evaluation environment
    safe_globals = {'__builtins__': None}
    safe_locals = SAFE_CALLABLES.copy()

    try:
        result = eval(compile(parsed, '<string>', mode='eval'), safe_globals, safe_locals)
    except Exception:
        return 'Error!'

    return str(result)
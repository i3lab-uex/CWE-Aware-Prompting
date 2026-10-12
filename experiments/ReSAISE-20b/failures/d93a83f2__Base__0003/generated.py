import ast

def safe_execute_code(snippet: str):
    """
    Execute a user-provided Python snippet safely.

    The function accepts only simple expressions (no statements, no imports,
    no assignments, no function definitions).  Only a small whitelist of
    built‑in functions and operators is permitted.  Any attempt to use disallowed
    syntax raises a ValueError.

    Parameters
    ----------
    snippet : str
        The Python expression to evaluate.

    Returns
    -------
    Any
        The result of evaluating the expression, or None if no value is produced.

    Raises
    ------
    ValueError
        If the snippet contains prohibited syntax or disallowed function calls.
    """

    # Whitelist of safe built‑in functions
    SAFE_BUILTINS = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
    }

    # Allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,      # top level expression
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,           # ternary
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,        # Python 3.8+: literal constants
        ast.Num,             # legacy numeric constants (for older Python)
        ast.Str,
        ast.Bytes,
        ast.Tuple,
        ast.List,
    }

    # Allowed binary operators
    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow
    }

    # Allowed unary operators
    ALLOWED_UNARYOPS = {
        ast.UAdd, ast.USub, ast.Not
    }

    # Allowed boolean operators
    ALLOWED_BOOLOPS = {
        ast.And, ast.Or
    }

    # Allowed comparison operators
    ALLOWED_CMPOPS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE
    }

    def _check(node: ast.AST):
        # Reject disallowed node types
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

        # Validate specific node types
        if isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_BINOPS:
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARYOPS:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        elif isinstance(node, ast.BoolOp):
            if type(node.op) not in ALLOWED_BOOLOPS:
                raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if type(op) not in ALLOWED_CMPOPS:
                    raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")
        elif isinstance(node, ast.Call):
            # Only allow calls to whitelisted names
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed function call: {ast.dump(node)}")
            # Recursively check arguments
            for arg in node.args:
                _check(arg)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                _check(elt)

        # Recurse into child nodes
        for child in ast.iter_child_nodes(node):
            _check(child)

    # Parse the snippet as an expression
    try:
        parsed = ast.parse(snippet, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Walk the AST and validate
    _check(parsed)

    # Evaluate safely with restricted globals
    try:
        result = eval(compile(parsed, filename='<safe_exec>', mode='eval'),
                      {'__builtins__': {}},
                      SAFE_BUILTINS)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None

    return result
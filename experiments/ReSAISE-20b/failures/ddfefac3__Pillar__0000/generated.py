import ast

# Whitelist of safe built‑in functions that students are allowed to use.
SAFE_BUILTINS = {
    'abs': abs,
    'len': len,
    'range': range,
    'min': min,
    'max': max,
    'sum': sum,
    # add more as needed
}

# Allowed AST node types.  Anything not listed will cause a ValueError.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.If,
    ast.For,
    ast.While,
    ast.Compare,
    ast.BoolOp,
    ast.Call,          # but only to allowed built‑ins
    ast.Attribute,     # for built‑in attributes like .__name__
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # Control flow nodes
    ast.Return,
    ast.Pass,
    ast.Break,
    ast.Continue,
}

# Operators that are considered safe
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.UAdd, ast.USub, ast.Not, ast.Invert,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
)

def _validate_node(node):
    """Recursively validate that the node is allowed."""
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Validate operators
    if isinstance(node, ast.BinOp) and type(node.op) not in SAFE_OPERATORS:
        raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.UnaryOp) and type(node.op) not in SAFE_OPERATORS:
        raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.BoolOp) and type(node.op) not in SAFE_OPERATORS:
        raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if type(op) not in SAFE_OPERATORS:
                raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")

    # Disallow function calls to anything other than the safe built‑ins
    if isinstance(node, ast.Call):
        # function must be a Name or Attribute pointing to a safe builtin
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                raise ValueError(f"Call to unsafe function: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # allow attributes of built‑ins (e.g., len.__name__)
            if not (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id in SAFE_BUILTINS
            ):
                raise ValueError(f"Unsafe attribute access: {ast.dump(node.func)}")
        else:
            raise ValueError("Unsupported call target type")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def process_python_code(code_str: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    Only a small, safe subset of the language is allowed.

    Parameters
    ----------
    code_str : str
        The Python source to execute.

    Returns
    -------
    Any
        Result of the last expression, or None if there is no output.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or operations.
    """
    # Parse into an AST, raising SyntaxError if invalid
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    # Validate the AST against our whitelist
    for node in parsed.body:
        _validate_node(node)

    # Prepare a restricted execution environment
    safe_globals = {"__builtins__": {}}
    safe_globals.update(SAFE_BUILTINS)

    # Execute the code
    try:
        exec(compile(parsed, filename="<sandbox>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    # Return the value of the last expression if present
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the same restricted environment
            return eval(compile(ast.Expression(node.value), filename="<sandbox>", mode="eval"), safe_globals)
    return None
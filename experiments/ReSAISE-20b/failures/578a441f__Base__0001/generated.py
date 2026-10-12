import ast

# List of AST node types that are disallowed in user scripts
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python 2; kept for completeness
    ast.Call,  # we allow calls to safe builtins only
    ast.Attribute,
    ast.Name,
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.For,
    ast.While,
    ast.If,
    ast.With,
    ast.Try,
    ast.Delete,
    ast.Global,
    ast.Nonlocal,
    ast.AugAssign,
    ast.Assign,
    ast.Raise,
    ast.Assert,
    ast.ImportFrom,
    ast.Import,
}

# Whitelist of safe built‑in functions/objects
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

def _check_syntax_and_security(code: str) -> ast.Module:
    """
    Parse the code and ensure it only contains a single expression
    with no disallowed nodes.
    """
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # The parsed AST must contain exactly one node, which must be an Expr
    if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.Expr):
        raise ValueError("Only a single expression is allowed in the script.")

    # Walk the tree to ensure no disallowed nodes appear
    for node in ast.walk(parsed):
        if isinstance(node, tuple(DISALLOWED_NODES)):
            # Allow Call nodes only to whitelisted builtins
            if isinstance(node, ast.Call):
                if not (
                    isinstance(node.func, ast.Name) and
                    node.func.id in SAFE_BUILTINS
                ):
                    raise ValueError("Disallowed function call detected.")
            else:
                raise ValueError(f"Disallowed construct: {type(node).__name__}")

    return parsed

def run_user_script(user_script: str):
    """
    Execute a user‑supplied Python expression in a sandboxed environment.

    Parameters
    ----------
    user_script : str
        The Python code supplied by the user. Must be a single expression.

    Returns
    -------
    Any
        The value resulting from evaluating the expression, or None if no value.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    parsed = _check_syntax_and_security(user_script)

    # Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}

    # Evaluate the expression node
    expr_node = parsed.body[0].value
    try:
        return eval(compile(ast.Expression(expr_node), "<user_script>", mode="eval"),
                    sandbox_globals, {})
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from None
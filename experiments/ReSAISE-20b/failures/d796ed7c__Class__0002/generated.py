import ast

# Allowed AST node types for a safe mathematical expression
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.USub,
    ast.UAdd,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.Paren := ast.Tuple,  # parentheses are handled by grouping
}

# Disallow any node that could lead to code execution or side effects
_DISALLOWED_NODES = {
    ast.Call,
    ast.Name,
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.Import,
    ast.ImportFrom,
    ast.Global,
    ast.Nonlocal,
    ast.ClassDef,
    ast.Module,
    ast.Assign,
    ast.AugAssign,
    ast.Delete,
}

def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if an illegal node is found.
    """
    if type(node) in _DISALLOWED_NODES:
        raise ValueError(f"Disallowed operation: {type(node).__name__}")
    if not isinstance(node, tuple(_ALLOWED_NODES)):
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _validate_ast(child)

def secure_math_eval(exp_str: str) -> float:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    exp_str : str
        The arithmetic expression to evaluate. Allowed characters are digits,
        whitespace, and the operators + - * / % ** // << >> | ^ &. Parentheses
        are permitted for grouping.

    Returns
    -------
    float
        The result of the evaluated expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, functions, or any unsafe
        construct. Also raised for syntax errors.
    """
    if not isinstance(exp_str, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    exp_str = exp_str.strip()
    if not exp_str:
        raise ValueError("Empty expression")

    # Parse into an AST
    try:
        parsed = ast.parse(exp_str, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the AST for safety
    _validate_ast(parsed)

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(parsed, filename="<secure_eval>", mode="eval"), {}, {})
    except Exception as exc:
        # Any exception during evaluation is considered unsafe
        raise ValueError(f"Evaluation error: {exc}") from None

    return result
import ast

ALLOWED_NODES = {
    # Expressions and literals
    ast.Expression,
    ast.Constant,          # Python 3.8+ for numbers, strings, etc.
    ast.Num,               # Legacy numeric literal
    ast.Str,
    ast.Bytes,
    ast.NameConstant,

    # Containers (optional, but safe)
    ast.Tuple,
    ast.List,
    ast.Dict,

    # Operations
    ast.BinOp,            # Binary operations (+, -, *, /, etc.)
    ast.UnaryOp,          # Unary operations (-, +)
    ast.BoolOp,           # Boolean operations (and, or)
    ast.Compare,          # Comparisons

    # Specific operator nodes
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,

    ast.UAdd,
    ast.USub,
    ast.Not,

    ast.And,
    ast.Or,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,

    # Parentheses
    ast.Paren,            # Not a real node, but included for clarity (ignored)
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively ensure that every node in the AST is from the allowed set.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluates a simple mathematical or logical expression provided as a string.
    
    Parameters
    ----------
    input_expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Processing Failed!' if unsafe.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure the entire tree is safe
        if not _is_safe(parsed):
            return 'Processing Failed!'

        # Evaluate the expression in a restricted environment
        result = eval(compile(parsed, filename="<ast>", mode="eval"), {}, {})
        return str(result)
    except Exception:
        # Any exception, including SyntaxError or TypeError, is treated as a failure
        return 'Processing Failed!'
import ast

# Allowed AST node types for a safe expression.
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,          # disallowed explicitly
    ast.Name,          # disallowed explicitly
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # literals
    ast.Num,           # Python <3.8
    ast.Constant,      # Python >=3.8
    ast.NameConstant,
    ast.List, ast.Tuple, ast.Dict, ast.Set,
}

# Operators we consider safe
_ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.UAdd, ast.USub,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.And, ast.Or,
}

def _is_safe_node(node):
    """
    Recursively check that the node and all its children are allowed.
    """
    if type(node) not in _ALLOWED_NODES:
        return False
    # Check operators specifically for BinOp, UnaryOp, BoolOp, Compare
    if isinstance(node, ast.BinOp):
        return type(node.op) in _ALLOWED_OPERATORS and _is_safe_node(node.left) and _is_safe_node(node.right)
    if isinstance(node, ast.UnaryOp):
        return type(node.op) in _ALLOWED_OPERATORS and _is_safe_node(node.operand)
    if isinstance(node, ast.BoolOp):
        return type(node.op) in _ALLOWED_OPERATORS and all(_is_safe_node(v) for v in node.values)
    if isinstance(node, ast.Compare):
        return all(type(op) in _ALLOWED_OPERATORS for op in node.ops) and \
               _is_safe_node(node.left) and all(_is_safe_node(comp) for comp in node.comparators)
    if isinstance(node, ast.Call):
        # disallow function calls
        return False
    if isinstance(node, ast.Name):
        # disallow variable names
        return False
    if isinstance(node, (ast.Attribute, ast.Subscript)):
        # disallow attribute access and subscription
        return False
    if isinstance(node, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
        return all(_is_safe_node(v) for v in getattr(node, 'elts', []))
    # For literals and other simple nodes
    return True

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the user.
    
    Parameters
    ----------
    quiz_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or 'Error!'
        if the expression is unsafe or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(quiz_expr, mode='eval')
    except SyntaxError:
        return 'Error!'

    # Validate the AST
    if not _is_safe_node(parsed):
        return 'Error!'

    try:
        # Evaluate with no globals or locals to avoid access to builtins
        result = eval(compile(parsed, '<string>', 'eval'), {}, {})
    except Exception:
        return 'Error!'

    return str(result)
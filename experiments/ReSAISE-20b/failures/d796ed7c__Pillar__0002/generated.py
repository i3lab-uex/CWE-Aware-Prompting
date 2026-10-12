import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node):
    """
    Recursively evaluate an AST node that has been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_func = _ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return op_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_func = _ALLOWED_UNARY.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return op_func(operand)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.Paren):
        return _eval(node.value)
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def _validate_ast(tree):
    """
    Walk the AST and ensure only allowed nodes are present.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                             ast.Num, ast.Constant)):
            continue
        elif isinstance(node, (ast.Module, ast.Expr)):
            # These are structural nodes that should be ignored
            continue
        else:
            raise ValueError(f"Disallowed expression component: {ast.dump(node)}")

def secure_math_eval(exp_str: str):
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    exp_str : str
        The user-provided mathematical expression.

    Returns
    -------
    result : int or float
        The evaluated numeric result.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe operations.
    """
    # Strip whitespace to avoid hidden characters
    exp_str = exp_str.strip()

    if not exp_str:
        raise ValueError("Empty expression")

    # Parse the string into an AST
    try:
        tree = ast.parse(exp_str, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate the AST to ensure only safe nodes are present
    _validate_ast(tree)

    # Evaluate the validated AST
    return _eval(tree)
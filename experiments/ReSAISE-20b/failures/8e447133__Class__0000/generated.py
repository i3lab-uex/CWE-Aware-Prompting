import ast
from typing import Any

# Allowed AST node types for safe evaluation
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,
    ast.NameConstant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.Lt, ast.Le, ast.Gt, ast.Ge, ast.Eq, ast.NotEq,
    ast.And, ast.Or, ast.Not,
}

# Allowed operators mapped to functions
OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.LShift: lambda a, b: a << b,
    ast.RShift: lambda a, b: a >> b,
    ast.BitOr: lambda a, b: a | b,
    ast.BitXor: lambda a, b: a ^ b,
    ast.BitAnd: lambda a, b: a & b,
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

def _eval_node(node: ast.AST) -> Any:
    if type(node) not in ALLOWED_NODES:
        raise ValueError("Disallowed node: %s" % type(node).__name__)
    if isinstance(node, ast.Module):
        # Expect a single expression
        if len(node.body) != 1:
            raise ValueError("Only single expressions allowed")
        return _eval_node(node.body[0])
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.value
    if isinstance(node, ast.Str):
        return node.s
    if isinstance(node, ast.NameConstant):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = OPERATORS[type(node.op)]
        return op_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = OPERATORS[type(node.op)]
        return op_func(operand)
    raise ValueError("Unhandled node type: %s" % type(node).__name__)

def execute_user_input(user_code: str) -> str:
    """
    Safely evaluate simple arithmetic or string expressions provided by a user.

    Parameters
    ----------
    user_code : str
        The user supplied Python code string.  Only a single expression is allowed.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or 'Execution Blocked!'
        if the code contains disallowed constructs.
    """
    try:
        # Parse into an AST
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure the tree contains only allowed nodes
    for node in ast.walk(tree):
        if type(node) not in ALLOWED_NODES:
            return 'Execution Blocked!'

    try:
        result = _eval_node(tree)
        return str(result)
    except Exception:
        # Any error during evaluation results in a block
        return 'Execution Blocked!'
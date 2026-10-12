import ast
from typing import Any

# Define the set of allowed AST node types and operators
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for literals (Python 3.8+)
    ast.NameConstant, # True/False/None for older Python
    ast.BoolOp,
    ast.Compare,
    ast.Call,         # disallowed but kept for potential extension
}
ALLOWED_OPERATORS = {
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
    ast.Invert,
}
ALLOWED_COMPARE_OPERATORS = {
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn
}
ALLOWED_BOOLEAN_OPERATORS = {ast.And, ast.Or}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively check that the AST contains only safe nodes and operators.
    """
    if type(node) not in ALLOWED_NODES:
        return False

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            return False
    elif isinstance(node, ast.BoolOp):
        if type(node.op) not in ALLOWED_BOOLEAN_OPERATORS:
            return False
    elif isinstance(node, ast.Compare):
        if any(type(op) not in ALLOWED_COMPARE_OPERATORS for op in node.ops):
            return False

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression supplied by the user.
    
    Parameters
    ----------
    math_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(math_expr, mode='eval')

        # Ensure the tree only contains safe nodes/operators
        if not _is_safe(parsed):
            return 'Processing Failed!'

        # Compile the AST into a code object
        compiled = compile(parsed, filename='<user_expr>', mode='eval')

        # Evaluate in a restricted namespace
        result: Any = eval(compiled, {'__builtins__': None}, {})

        return str(result)
    except Exception:
        # Any exception (syntax, evaluation error, security violation) results in failure
        return 'Processing Failed!'
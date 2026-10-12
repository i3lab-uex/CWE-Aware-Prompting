import ast
import math

# Allowed nodes in the AST for a safe expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,   # Python 3.8+
    ast.Num,        # Backward compatibility
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
}

# Allowed operators
ALLOWED_OPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitAnd, ast.BitXor,
    ast.UAdd, ast.USub, ast.Not, ast.Invert,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
}

# Allowed function names from math module
ALLOWED_FUNCS = {name for name in dir(math) if not name.startswith('_')}

def _is_safe(node: ast.AST) -> bool:
    """Recursively check that all nodes are allowed."""
    if type(node) not in ALLOWED_NODES:
        return False
    if isinstance(node, ast.BinOp) or isinstance(node, ast.BoolOp) or isinstance(node, ast.Compare):
        for op in node.ops if hasattr(node, 'ops') else [node.op]:
            if type(op) not in ALLOWED_OPS:
                return False
    if isinstance(node, ast.Call):
        # Function name must be a Name node and in the allowed set
        if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_FUNCS:
            return False
        # All arguments must be safe
        for arg in node.args:
            if not _is_safe(arg):
                return False
    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple mathematical/logic expression.

    Parameters
    ----------
    formula : str
        The user supplied expression.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Processing Failed!' if unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(formula, mode='eval')
    except Exception:
        return 'Processing Failed!'

    # Validate the AST
    if not _is_safe(parsed):
        return 'Processing Failed!'

    # Build a safe evaluation environment
    safe_globals = {'__builtins__': None}
    safe_locals = {name: getattr(math, name) for name in ALLOWED_FUNCS}

    try:
        result = eval(compile(parsed, filename='<ast>', mode='eval'),
                      safe_globals, safe_locals)
    except Exception:
        return 'Processing Failed!'

    # Convert result to string
    try:
        return str(result)
    except Exception:
        return 'Processing Failed!'
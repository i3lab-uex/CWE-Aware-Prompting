import ast
import operator

# Mapping of allowed AST nodes to Python operators/functions
_allowed_nodes = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Call,
    ast.Load,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Tuple,
    ast.List,
}

# Allowed functions/operators (very small set)
_allowed_funcs = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
}

_allowed_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def _eval(node, context):
    if type(node) not in _allowed_nodes:
        raise ValueError(f"Disallowed node: {type(node).__name__}")

    if isinstance(node, ast.Expression):
        return _eval(node.body, context)

    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, context)
        right = _eval(node.right, context)
        op_func = _allowed_ops.get(type(node.op))
        if not op_func:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, context)
        op_func = _allowed_ops.get(type(node.op))
        if not op_func:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        return op_func(operand)

    if isinstance(node, ast.Name):
        if node.id in context:
            return context[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    if isinstance(node, ast.Call):
        func = _eval(node.func, context)
        args = [_eval(arg, context) for arg in node.args]
        kwargs = {kw.arg: _eval(kw.value, context) for kw in node.keywords}
        if not callable(func):
            raise ValueError(f"{func} is not callable")
        return func(*args, **kwargs)

    if isinstance(node, (ast.Tuple, ast.List)):
        return type(node)([_eval(elt, context) for elt in node.elts])

    if isinstance(node, ast.Subscript):
        value = _eval(node.value, context)
        idx = _eval(node.slice, context)
        return value[idx]

    if isinstance(node, ast.Index):
        return _eval(node.value, context)

    if isinstance(node, ast.Slice):
        lower = _eval(node.lower, context) if node.lower else None
        upper = _eval(node.upper, context) if node.upper else None
        step  = _eval(node.step,  0) if node.step  else None
        return slice(lower, upper, step)

    raise ValueError(f"Unhandled node type: {type(node).__name__}")

def evaluate_user_code(code_string: str) -> str:
    """
    Evaluate a user-provided Python expression safely.

    Parameters
    ----------
    code_string : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the result or an error message.
    """
    try:
        # Parse into AST
        parsed = ast.parse(code_string, mode='eval')

        # Validate all nodes are allowed
        for node in ast.walk(parsed):
            if type(node) not in _allowed_nodes:
                return 'Unsafe Code Detected!'

        # Build context with allowed functions and math constants
        import math
        context = {**_allowed_funcs, **{k: getattr(math, k) for k in dir(math) if not k.startswith('_')}}

        result = _eval(parsed, context)
        return str(result)

    except Exception:
        return 'Unsafe Code Detected!'
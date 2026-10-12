import ast

# Allowed AST node types for a safe expression
SAFE_NODES = {
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.IfExp,
    ast.Compare,
    ast.Call,        # only for whitelisted functions
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.Num,         # Python <3.8
    ast.Str,
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Set,
    ast.Dict,
}

# Whitelisted functions (can be extended if needed)
SAFE_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
}

def _is_safe_node(node):
    """Recursively check if a node and its children are safe."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def _eval(node, context=None):
    """Evaluate a safe AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, context)
    elif isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.Num):      # Python <3.8
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Bytes):
        return node.s
    elif isinstance(node, ast.Tuple):
        return tuple(_eval(elt, context) for elt in node.elts)
    elif isinstance(node, ast.List):
        return [_eval(elt, context) for elt in node.elts]
    elif isinstance(node, ast.Set):
        return {_eval(elt, context) for elt in node.elts}
    elif isinstance(node, ast.Dict):
        return {_eval(k, context): _eval(v, context) for k, v in zip(node.keys, node.values)}
    elif isinstance(node, ast.Name):
        if context and node.id in context:
            return context[node.id]
        raise ValueError(f"Name {node.id} not allowed")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left, context)
        right = _eval(node.right, context)
        return eval(compile(ast.Expression(node), filename="<ast>", mode="eval"))
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, context)
        return eval(compile(ast.Expression(node), filename="<ast>", mode="eval"))
    elif isinstance(node, ast.BoolOp):
        return eval(compile(ast.Expression(node), filename="<ast>", mode="eval"))
    elif isinstance(node, ast.Compare):
        return eval(compile(ast.Expression(node), filename="<ast>", mode="eval"))
    elif isinstance(node, ast.IfExp):
        return eval(compile(ast.Expression(node), filename="<ast>", mode="eval"))
    elif isinstance(node, ast.Call):
        func = _eval(node.func, context)
        if func not in SAFE_FUNCTIONS.values():
            raise ValueError("Function not allowed")
        args = [_eval(arg, context) for arg in node.args]
        kwargs = {kw.arg: _eval(kw.value, context) for kw in node.keywords}
        return func(*args, **kwargs)
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")

def process_user_input(user_query: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    user_query : str
        The string containing the expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Error!' on failure.
    """
    try:
        # Parse the expression
        parsed = ast.parse(user_query, mode='eval')

        # Ensure all nodes are safe
        if not _is_safe_node(parsed):
            return 'Error!'

        # Evaluate with an empty context (no globals)
        result = _eval(parsed, context={})
        return str(result)
    except Exception:
        # Any exception (syntax, safety, runtime) results in a generic error
        return 'Error!'
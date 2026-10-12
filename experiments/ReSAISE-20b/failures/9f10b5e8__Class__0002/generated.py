import ast

# Allowed AST node types for a safe expression evaluator
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant, # True/False/None in older versions
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
}

# Mapping of operator nodes to actual functions
OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.USub: lambda a: -a,
    ast.UAdd: lambda a: +a,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: lambda a: not a,
    ast.Eq: lambda a, b: a == b,
    ast.NotEq: lambda a, b: a != b,
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Constant):          # Python 3.8+
        return node.value
    if isinstance(node, ast.Num):               # Python <3.8
        return node.n
    if isinstance(node, ast.NameConstant):      # True/False/None in older Python
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

    if isinstance(node, ast.BoolOp):
        values = [_eval_node(v) for v in node.values]
        op_func = OPERATORS[type(node.op)]
        result = values[0]
        for v in values[1:]:
            result = op_func(result, v)
        return result

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left)
        # Only support single comparator for simplicity
        if len(node.comparators) != 1 or len(node.ops) != 1:
            raise ValueError("Complex comparisons not allowed")
        right = _eval_node(node.comparators[0])
        op_func = OPERATORS[type(node.ops[0])]
        return op_func(left, right)

    if isinstance(node, (ast.List, ast.Tuple)):
        return [_eval_node(e) for e in node.elts]

    if isinstance(node, ast.Dict):
        keys = [_eval_node(k) for k in node.keys]
        values = [_eval_node(v) for v in node.values]
        return dict(zip(keys, values))

    if isinstance(node, ast.Set):
        return {_eval_node(e) for e in node.elts}

    raise ValueError(f"Unsupported node type: {type(node).__name__}")

def _is_safe_ast(tree):
    """
    Walk the AST and ensure all nodes are in ALLOWED_NODES.
    Reject any node that references names (variables, functions).
    """
    for node in ast.walk(tree):
        if type(node) not in ALLOWED_NODES:
            return False
        # Disallow any Name nodes (variable/function access)
        if isinstance(node, ast.Name):
            return False
    return True

def run_user_query(query: str) -> str:
    """
    Safely evaluate a user-provided query string.

    Parameters
    ----------
    query : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Error!' if any issue occurs.
    """
    try:
        # Parse as an expression (no statements)
        tree = ast.parse(query, mode='eval')
    except Exception:
        return 'Error!'

    if not _is_safe_ast(tree):
        return 'Error!'

    try:
        result = _eval_node(tree.body)
        return str(result)
    except Exception:
        return 'Error!'
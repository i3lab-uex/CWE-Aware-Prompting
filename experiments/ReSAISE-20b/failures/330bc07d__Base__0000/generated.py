import ast

# Define the set of AST node types that are considered safe for evaluation.
SAFE_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.NameConstant,  # True, False, None
    ast.Num,           # Python <3.8 numeric literals
    ast.Constant,      # Python >=3.8 constants (int, float, str, bool, None)
    ast.Str,
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,
    # Allowed operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.UAdd, ast.USub, ast.Not, ast.Invert,
    ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
    ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
    # Name node for accessing built-in constants (e.g., True, False, None)
    ast.Name,
}

# Whitelist of names that can be used in the expression
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that every node in the AST is allowed."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def _eval_ast(node: ast.AST, names: dict):
    """Evaluate a safe AST node using the provided name mapping."""
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body, names)
    elif isinstance(node, ast.Constant):  # Python >=3.8
        return node.value
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Bytes):
        return node.s
    elif isinstance(node, ast.NameConstant):  # True, False, None for older Python
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval_ast(node.left, names)
        right = _eval_ast(node.right, names)
        return eval(f"{left} {node.op.__class__.__name__} {right}")  # safe ops only
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand, names)
        return eval(f"{node.op.__class__.__name__} {operand}")
    elif isinstance(node, ast.BoolOp):
        values = [_eval_ast(v, names) for v in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        else:  # Or
            return any(values)
    elif isinstance(node, ast.Compare):
        left = _eval_ast(node.left, names)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval_ast(comparator, names)
            if isinstance(op, ast.Eq):
                if left != right:
                    return False
            elif isinstance(op, ast.NotEq):
                if left == right:
                    return False
            elif isinstance(op, ast.Lt):
                if not (left < right):
                    return False
            elif isinstance(op, ast.LtE):
                if not (left <= right):
                    return False
            elif isinstance(op, ast.Gt):
                if not (left > right):
                    return False
            elif isinstance(op, ast.GtE):
                if not (left >= right):
                    return False
            elif isinstance(op, ast.Is):
                if left is not right:
                    return False
            elif isinstance(op, ast.IsNot):
                if left is right:
                    return False
            elif isinstance(op, ast.In):
                if not (left in right):
                    return False
            elif isinstance(op, ast.NotIn):
                if left in right:
                    return False
            else:
                raise ValueError("Unsupported comparison operator")
            left = right
        return True
    elif isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        raise ValueError(f"Use of name '{node.id}' is not allowed")
    elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        elts = [_eval_ast(e, names) for e in node.elts]
        if isinstance(node, ast.List):
            return elts
        elif isinstance(node, ast.Tuple):
            return tuple(elts)
        else:
            return set(elts)
    elif isinstance(node, ast.Dict):
        keys = [_eval_ast(k, names) for k in node.keys]
        values = [_eval_ast(v, names) for v in node.values]
        return dict(zip(keys, values))
    else:
        raise ValueError("Unsupported AST node type")

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user-provided Python expression and return the result as a string.
    
    Parameters:
        query_expr (str): The expression to evaluate.
    
    Returns:
        str: The string representation of the result, or 'Error!' if evaluation fails
             or the expression is unsafe.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(query_expr, mode='eval')
        
        # Ensure the entire tree contains only safe nodes
        if not _is_safe_node(parsed):
            return 'Error!'
        
        # Evaluate the expression using only allowed names
        result = _eval_ast(parsed, ALLOWED_NAMES)
        
        return str(result)
    except Exception:
        # Any exception (syntax error, unsafe node, runtime error) results in 'Error!'
        return 'Error!'
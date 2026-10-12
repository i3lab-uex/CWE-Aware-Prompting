import ast
import operator

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    # Logical operators
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
    # Comparisons
    ast.Eq: lambda a, b: a == b,
    ast.NotEq: lambda a, b: a != b,
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
)

def _eval(node):
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value
    if isinstance(node, ast.Tuple):
        return tuple(_eval(e) for e in node.elts)
    if isinstance(node, ast.List):
        return [_eval(e) for e in node.elts]
    if isinstance(node, ast.Dict):
        return {_eval(k): _eval(v) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Set):
        return {_eval(e) for e in node.elts}
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
    if isinstance(node, ast.BoolOp):
        values = [_eval(v) for v in node.values]
        op_type = type(node.op)
        if op_type is ast.And:
            return all(values)
        if op_type is ast.Or:
            return any(values)
    if isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            op_type = type(op)
            if op_type in _ALLOWED_OPERATORS:
                if not _ALLOWED_OPERATORS[op_type](left, right):
                    return False
            else:
                raise ValueError("Unsupported comparison operator")
            left = right
        return True
    if isinstance(node, ast.NameConstant):
        return node.value
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a user supplied arithmetic or logical expression.
    
    Parameters
    ----------
    math_expr : str
        Expression to evaluate.

    Returns
    -------
    str
        Result of evaluation converted to string, or 'Processing Failed!'
        if any error occurs or the expression contains disallowed syntax.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(math_expr, mode='eval')
        
        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'
        
        result = _eval(parsed.body)
        return str(result)
    except Exception:
        # Catch any parsing or evaluation error
        return 'Processing Failed!'
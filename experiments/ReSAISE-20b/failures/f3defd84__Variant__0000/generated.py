import ast
import operator

# Mapping of supported operators to their corresponding functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression, ast.Module, ast.Expr,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.NameConstant, ast.Num, ast.Constant,  # for literals
)

# Allowed names (e.g., True, False)
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float, bool)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        else:
            raise ValueError(f"Use of name '{node.id}' is not allowed")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        else:
            raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        else:
            raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.BoolOp):
        values = [_eval(v) for v in node.values]
        op_type = type(node.op)
        if op_type is ast.And:
            return all(values)
        elif op_type is ast.Or:
            return any(values)
        else:
            raise ValueError("Unsupported boolean operator")
    if isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            op_type = type(op)
            if op_type in OPERATORS:
                if not OPERATORS[op_type](left, right):
                    return False
                left = right  # for chained comparisons
            else:
                raise ValueError("Unsupported comparison operator")
        return True
    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression.
    Returns the result as a string, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(expression, mode='eval')
        # Verify all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
        result = _eval(parsed.body)
        return str(result)
    except Exception:
        # Any error results in the generic failure message
        return "Processing Failed!"
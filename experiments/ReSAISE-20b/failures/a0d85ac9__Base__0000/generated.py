import ast
import operator

# Mapping of allowed AST operators to corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level expression container
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.NameConstant,  # True/False/None
    ast.Num,
    ast.Constant,     # Python 3.8+ constants (int, float, str, bool)
    ast.Name,
)

# Allowed names
_ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    """Recursively evaluate an AST node, only allowing safe operations."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float, bool)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Disallowed name: {node.id}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Disallowed binary operator: {op_type}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Disallowed unary operator: {op_type}")

    if isinstance(node, ast.BoolOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed boolean operator: {op_type}")
        values = [_eval(v) for v in node.values]
        # Reduce with the operator
        result = values[0]
        for v in values[1:]:
            result = _ALLOWED_OPERATORS[op_type](result, v)
        return result

    if isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            op_type = type(op)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed comparison operator: {op_type}")
            if not _ALLOWED_OPERATORS[op_type](left, right):
                return False
            left = right
        return True

    raise ValueError(f"Unsupported AST node: {type(node)}")

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a user-supplied arithmetic or logical expression.

    Parameters
    ----------
    input_expr : str
        Expression to evaluate.

    Returns
    -------
    str
        Result of the expression as a string, or 'Processing Failed!' on error.
    """
    try:
        # Parse the expression to an AST node
        parsed = ast.parse(input_expr, mode='eval')

        # Verify all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        # Evaluate the parsed AST
        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any exception leads to a safe failure response
        return 'Processing Failed!'
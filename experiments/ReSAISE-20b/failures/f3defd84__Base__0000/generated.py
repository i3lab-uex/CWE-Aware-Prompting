import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.NameConstant,
    ast.Name,
)

# Allowed names (only constants like True, False, None)
_ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None,
}

def _eval(node):
    """
    Recursively evaluate an AST node, only if it is composed of allowed
    nodes and operators.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Numeric literals
        return node.n if hasattr(node, "n") else node.value

    if isinstance(node, ast.Name):
        # Only allow predefined constants
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name {node.id} not allowed")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")

    if isinstance(node, ast.BoolOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Bool operator {op_type} not allowed")
        values = [_eval(v) for v in node.values]
        # Reduce the bool operation
        result = values[0]
        for v in values[1:]:
            result = _ALLOWED_OPERATORS[op_type](result, v)
        return result

    if isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op_node, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            op_type = type(op_node)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Compare operator {op_type} not allowed")
            if not _ALLOWED_OPERATORS[op_type](left, right):
                return False
            left = right
        return True

    raise ValueError(f"Unsupported node type: {type(node)}")

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluate a user supplied arithmetic or logical expression.
    
    Parameters
    ----------
    expression : str
        The expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Processing Failed!' if any
        error occurs or the expression contains unsafe constructs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        # Evaluate the parsed expression
        result = _eval(parsed)

        return str(result)
    except Exception:
        # Any exception is treated as a failure
        return 'Processing Failed!'
import ast
import operator

# Mapping of AST operators to actual functions
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
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or:  lambda a, b: a or b,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.NameConstant,  # True, False, None
    ast.Num,          # Python <3.8 numbers
    ast.Constant,     # Python 3.8+ constants
    ast.Name,
)

# Allowed names (variables/constants)
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value
    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Disallowed name: {node.id}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
    elif isinstance(node, ast.BoolOp):
        values = [_eval(v) for v in node.values]
        op_type = type(node.op)
        if op_type is ast.And:
            return all(values)
        elif op_type is ast.Or:
            return any(values)
    elif isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            op_type = type(op)
            if op_type in OPERATORS:
                left = OPERATORS[op_type](left, right)
            else:
                raise ValueError(f"Unsupported comparator: {op}")
        return left
    # If node type is not allowed, raise error
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_input_expression(expression: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression.
    
    Parameters
    ----------
    expression : str
        The user-supplied expression to evaluate.
    
    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' if any error occurs.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(expression, mode='eval')
        
        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Node type {type(node).__name__} is not allowed.")
        
        # Evaluate the parsed AST
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any exception leads to failure message
        return 'Processing Failed!'
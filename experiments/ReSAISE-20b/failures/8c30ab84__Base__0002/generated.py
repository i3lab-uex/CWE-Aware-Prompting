import ast
import operator

# Mapping of allowed AST operators to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,  # top level node for eval()
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Tuple,
    ast.List,
    ast.Subscript,    # to allow indexing if needed
)

def _eval_node(node):
    """Recursively evaluate an AST node, only allowing safe operations."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # Allow numbers only
        value = node.n if hasattr(node, "n") else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value)}")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    if isinstance(node, (ast.Tuple, ast.List)):
        return tuple(_eval_node(e) for e in node.elts)

    if isinstance(node, ast.Subscript):
        # Allow indexing into tuples/lists
        value = _eval_node(node.value)
        slice_ = node.slice
        if isinstance(slice_, ast.Index):
            index = _eval_node(slice_.value)
            return value[index]
        elif isinstance(slice_, ast.Slice):
            start = _eval_node(slice_.lower) if slice_.lower else None
            stop = _eval_node(slice_.upper) if slice_.upper else None
            step = _eval_node(slice_.step) if slice_.step else None
            return value[slice(start, stop, step)]
        else:
            raise ValueError("Unsupported subscript type")

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def compute_expression(expression_input: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expression_input : str
        The user-provided mathematical expression to evaluate.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe constructs.
    """
    if not isinstance(expression_input, str):
        raise ValueError("Expression must be a string")

    # Parse expression into an AST
    try:
        parsed = ast.parse(expression_input, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    return _eval_node(parsed.body)
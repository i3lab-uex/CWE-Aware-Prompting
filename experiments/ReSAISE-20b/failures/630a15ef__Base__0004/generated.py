import ast
import operator as op

# Mapping of allowed AST operator nodes to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Constant,   # Python 3.8+
    ast.Num,        # for older versions
)


def _validate_node(node: ast.AST) -> None:
    """
    Recursively validate that the AST contains only safe nodes.
    Raises ValueError if an unsafe node is found.
    """
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    # Validate operator types
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed operator: {ast.dump(node.op)}")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {ast.dump(node.op)}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _validate_node(child)


def _eval_node(node: ast.AST) -> float:
    """
    Recursively evaluate a validated AST node.
    Returns the numerical result.
    """
    if isinstance(node, ast.Constant):  # Python 3.8+
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        return node.value
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_func = _ALLOWED_OPERATORS[type(node.op)]
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_func = _ALLOWED_OPERATORS[type(node.op)]
        return operator_func(operand)

    raise ValueError(f"Unsupported node type during evaluation: {type(node)}")


def process_user_query(query: str):
    """
    Evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    query : str
        The user-provided mathematical expression.

    Returns
    -------
    float or int
        The computed result of the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe characters, disallowed syntax,
        or if the expression is malformed.
    ZeroDivisionError
        Propagated from Python's arithmetic operations when division by zero occurs.
    """
    if not isinstance(query, str):
        raise ValueError("Query must be a string")

    stripped = query.strip()
    if not stripped:
        raise ValueError("Empty expression is not allowed")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(stripped, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Malformed expression: {e}")

    # Validate the AST for safety
    _validate_node(parsed)

    # Evaluate the validated AST
    return _eval_node(parsed.body)
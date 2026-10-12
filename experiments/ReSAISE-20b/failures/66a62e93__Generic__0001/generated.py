import ast
import operator

# Mapping of supported binary operators to their functions
BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of supported unary operators to their functions
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user supplied Python expression that may contain
    simple arithmetic or string operations.

    Parameters
    ----------
    code_string : str
        The user supplied expression.  Only literals, arithmetic operators,
        and string concatenation are permitted.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or
        'Execution Blocked!' if the expression contains unsafe constructs.
    """
    try:
        # Parse into an AST.  We only allow a single expression.
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Ensure the tree contains only allowed nodes
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.Constant, ast.BinOp,
                             ast.UnaryOp, ast.NameConstant)):
            continue
        # Allow string concatenation via BinOp with Add
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            continue
        # Disallow everything else
        return 'Execution Blocked!'

    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.NameConstant):  # True/False/None in older Python
            return node.value
        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)
            if op_type not in BIN_OPS:
                raise ValueError('Unsupported binary operator')
            return BIN_OPS[op_type](left, right)
        if isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in UNARY_OPS:
                raise ValueError('Unsupported unary operator')
            return UNARY_OPS[op_type](operand)
        raise ValueError('Unsupported node type')

    try:
        result = eval_node(tree.body)
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to a string representation
    return str(result)
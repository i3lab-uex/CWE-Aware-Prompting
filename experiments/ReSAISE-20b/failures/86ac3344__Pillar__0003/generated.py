import ast
import operator as op

# Supported operators mapping from AST node to actual Python operation
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 for numbers
    ast.Tuple,
    ast.List,
    ast.Call,        # We disallow calls but keep node type for detection
)

def _validate_node(node):
    """
    Recursively validate that the AST node contains only allowed constructs.
    Raises ValueError if an unsafe construct is found.
    """
    # Reject any node type not in the allowed list
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    # Reject function calls or attribute access
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")

    # Validate operator types
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    # Recursively validate child nodes
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def _evaluate_ast(node):
    """
    Evaluate the validated AST node recursively.
    """
    if isinstance(node, ast.Expression):
        return _evaluate_ast(node.body)

    if isinstance(node, (ast.Num,)):
        # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):
        # Python >=3.8
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _evaluate_ast(node.left)
        right = _evaluate_ast(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate_ast(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    if isinstance(node, (ast.Tuple, ast.List)):
        # Evaluate elements but disallow any non-numeric types
        return [_evaluate_ast(el) for el in node.elts]

    raise ValueError(f"Unsupported AST node during evaluation: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    exp : str
        User-provided mathematical expression.

    Returns
    -------
    result : int or float
        The evaluated numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax, characters, or unsafe constructs.
    """
    if not isinstance(exp, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to simplify validation
    exp = exp.strip()
    if not exp:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST for safety
    _validate_node(parsed)

    # Evaluate the validated AST
    return _evaluate_ast(parsed)
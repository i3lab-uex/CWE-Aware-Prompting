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
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Expr,
    ast.Module,
)

# Disallowed names (e.g., math functions, builtins)
_DISALLOWED_NAMES = {
    'eval', 'exec', 'compile', '__import__',
    # add more if needed
}

def _validate_node(node: ast.AST):
    """Recursively validate that the AST node contains only allowed constructs."""
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    if isinstance(node, ast.Call):
        # disallow any function calls
        raise ValueError("Function calls are not allowed")
    if isinstance(node, ast.Name):
        if node.id in _DISALLOWED_NAMES:
            raise ValueError(f"Use of disallowed name: {node.id}")

    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def _eval_ast(node: ast.AST) -> float:
    """Recursively evaluate the validated AST node."""
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
    raise ValueError(f"Unhandled node type during evaluation: {type(node).__name__}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    exp : str
        User-provided mathematical expression (e.g., "2 * (3 + 4)").

    Returns
    -------
    float or int
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, nodes,
        or constructs that could lead to code injection.
    """
    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Validate the AST for safety
    _validate_node(parsed)

    # Evaluate the safe AST
    return _eval_ast(parsed)
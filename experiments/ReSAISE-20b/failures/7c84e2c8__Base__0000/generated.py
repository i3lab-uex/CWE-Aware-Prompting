import ast
import operator

# Map AST operators to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level expression
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8
    ast.Expr,
    ast.Module,
    ast.Load,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Num):          # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):     # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    # If we reach here, node type is not allowed
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def _validate_ast(tree):
    """
    Walk the AST and ensure that all nodes are allowed.
    Raises ValueError if any disallowed node is found.
    """
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        # Ensure that operators are allowed
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            op_type = type(node.op)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed operator: {op_type.__name__}")

def calculate_user_input(user_input: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    user_input : str
        The user's mathematical expression (e.g., "2 + 3 * (4 - 1)").

    Returns
    -------
    float or int
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains disallowed characters, syntax errors,
        or unsupported operations.
    """
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to reduce trivial errors
    expr = user_input.strip()
    if not expr:
        raise ValueError("Input string is empty")

    try:
        # Parse expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Validate the AST for safety
    _validate_ast(tree)

    # Evaluate the validated AST
    return _eval_node(tree.body)
import ast
import operator

# Mapping of allowed AST operators to the corresponding Python functions
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
}

# Allowed node types for the expression
_ALLOWED_NODE_TYPES = (
    ast.Expression,  # top-level wrapper
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 (numbers)
    ast.Tuple,
    ast.List,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, (ast.Tuple, ast.List)):
        # Evaluate each element
        return type(node)([_eval_node(elt) for elt in node.elts])

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def _validate_ast(tree):
    """
    Walk the AST and ensure that only allowed node types and operators are present.
    Raises ValueError if any disallowed element is found.
    """
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODE_TYPES):
            raise ValueError(f"Disallowed AST node: {type(node).__name__}")

        if isinstance(node, ast.BinOp) and type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")

        if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

        if isinstance(node, ast.Call):
            # No function calls are allowed
            raise ValueError("Function calls are not permitted in expressions")

def secure_math_eval(expr_str: str):
    """
    Evaluate a mathematical expression securely.

    Parameters
    ----------
    expr_str : str
        The user-provided string containing a mathematical expression.

    Returns
    -------
    result : int | float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsafe characters, unsupported operations,
        or if the expression is malformed.
    """
    # Basic sanity check: empty string
    if not expr_str or not isinstance(expr_str, str):
        raise ValueError("Input must be a non-empty string")

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr_str, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Validate the AST
    _validate_ast(tree)

    # Evaluate the expression recursively
    return _eval_node(tree.body)
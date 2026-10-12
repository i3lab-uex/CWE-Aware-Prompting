import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed AST unary operators to functions
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.NameConstant, # True/False/None in older versions
)

def _validate_node(node: ast.AST) -> None:
    """
    Recursively validate that a node and all its children are allowed.
    Raises ValueError if an unsafe or unsupported construct is found.
    """
    # Check node type
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

    # Check operators
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")

    # Recurse into children
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def _eval_node(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node. Assumes validation has already
    taken place.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # <3.8
        return node.n

    if isinstance(node, ast.Constant):  # >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _ALLOWED_UNARY_OPERATORS[type(node.op)]
        return op_func(operand)

    raise ValueError(f"Unhandled node type during evaluation: {type(node).__name__}")

def secure_math_eval(expr_str: str) -> float:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_str : str
        The arithmetic expression to evaluate. Only basic binary and unary
        operators (+, -, *, /, //, %, **), numeric literals, and parentheses
        are allowed. No function calls or variable names may be used.

    Returns
    -------
    float
        The numeric result of the expression.

    Raises
    ------
    ValueError
        If the input contains disallowed syntax, operators, or is otherwise
        malformed.
    ZeroDivisionError
        Propagated from the underlying arithmetic operations if division by zero occurs.
    """
    # Strip leading/trailing whitespace
    expr_str = expr_str.strip()
    if not expr_str:
        raise ValueError("Empty expression")

    try:
        # Parse expression in eval mode
        parsed = ast.parse(expr_str, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the parsed AST
    _validate_node(parsed)

    # Evaluate safely
    return _eval_node(parsed)
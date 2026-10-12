import ast
import operator as op

# Supported operators mapping to the corresponding Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,        # Python <3.8
    ast.Constant,   # Python >=3.8
    ast.Tuple,
    ast.List,
)

def _evaluate(node: ast.AST) -> float:
    """
    Recursively evaluate an AST node that represents a numeric expression.
    Raises ValueError if the node type or operator is not supported.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Python 3.8+ uses Constant; older uses Num
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _evaluate(node.operand)
        return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    # If we reach here, the node type is not allowed
    raise ValueError(f"Unsupported expression component: {type(node).__name__}")

def compute_expression(input_expr: str) -> float:
    """
    Parse and evaluate a simple arithmetic expression supplied as a string.
    
    Parameters
    ----------
    input_expr : str
        The arithmetic expression to evaluate. Only numbers and the operators
        +, -, *, /, //, %, ** are allowed.

    Returns
    -------
    float
        The numerical result of evaluating the expression.

    Raises
    ------
    ValueError
        If the input contains unsupported characters, unsafe operations,
        or malformed syntax.
    """
    if not isinstance(input_expr, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to reduce noise
    expr = input_expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure all nodes in the tree are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _evaluate(parsed.body)

    return result
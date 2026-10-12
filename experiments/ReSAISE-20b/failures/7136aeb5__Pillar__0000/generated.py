import ast
import operator as op

# Allowed operators mapping to actual functions
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
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Tuple,
    ast.List,
    ast.Load,
)

def _eval_node(node):
    """
    Recursively evaluate an AST node after validating its type.
    Raises ValueError on disallowed nodes or operators.
    """
    if isinstance(node, (ast.Num, ast.Constant)):
        # Accept numbers only
        value = node.n if hasattr(node, "n") else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    if isinstance(node, (ast.Tuple, ast.List)):
        # Evaluate elements in a tuple/list
        return type(node)([_eval_node(elt) for elt in node.elts])

    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_expression_safely(expr: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate. Only basic arithmetic
        operators (+, -, *, /, //, %, **), parentheses, and numeric literals
        are allowed. No variables or function calls are permitted.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax, unsupported nodes,
        or invalid formatting.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate that the AST only contains allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression
    return _eval_node(parsed.body)
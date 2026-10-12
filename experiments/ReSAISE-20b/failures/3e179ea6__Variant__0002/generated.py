import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Tuple,
    ast.List,
)

def _evaluate(node: ast.AST):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if an unsupported node or operator is encountered.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, constants can be of many types; only allow numbers
        value = node.n if hasattr(node, 'n') else node.value
        if isinstance(value, (int, float)):
            return value
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} is not allowed")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} is not allowed")

    if isinstance(node, (ast.Tuple, ast.List)):
        # Allow tuples/lists of numbers
        return type(node)([_evaluate(elt) for elt in node.elts])

    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluate a mathematical expression given as a string.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result or
        'Unsafe Code Detected!' if the expression contains disallowed content.
    """
    try:
        # Parse the expression in 'eval' mode to ensure it's a single expression
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Verify that all nodes in the parsed AST are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            return 'Unsafe Code Detected!'

    try:
        result = _evaluate(parsed)
        return str(result)
    except Exception:
        # Any error during evaluation is treated as unsafe
        return 'Unsafe Code Detected!'
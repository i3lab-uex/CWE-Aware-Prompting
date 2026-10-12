import ast
import operator as op

# Mapping of allowed AST operator nodes to actual Python functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # top-level container
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python 3.8+
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Expr,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is numeric
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {operator_type.__name__}")
        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_type = type(node.op)
        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")
        return _ALLOWED_OPERATORS[operator_type](operand)

    # Disallow any function calls, names or other nodes
    raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_math_expression(expression: str):
    """
    Evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expression : str
        A user-provided mathematical expression containing only numbers,
        parentheses and the operators +, -, *, /, **, %, //.

    Returns
    -------
    float or int
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or unsafe operations.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the expression safely
    return _eval(parsed.body)
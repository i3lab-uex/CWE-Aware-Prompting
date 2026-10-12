import ast
import operator as op

# Mapping of AST operator nodes to actual Python operators
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
    ast.ParenExpr if hasattr(ast, "ParenExpr") else type(None),  # some ASTs
)

def _eval_node(node):
    """Recursively evaluate an allowed AST node."""
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def secure_eval_expression(exp: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    exp : str
        A user-provided string containing a mathematical expression.

    Returns
    -------
    int | float
        The evaluated result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters, operators,
        or if it attempts unsafe operations.
    """
    # Basic validation: allow only digits, operators, parentheses, decimal points, and whitespace
    allowed_chars = set("0123456789+-*/%() .\n\t")
    if any(ch not in allowed_chars for ch in exp):
        raise ValueError("Expression contains disallowed characters.")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(exp, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed AST node: {type(node).__name__}")

    # Evaluate the expression recursively
    return _eval_node(parsed.body)
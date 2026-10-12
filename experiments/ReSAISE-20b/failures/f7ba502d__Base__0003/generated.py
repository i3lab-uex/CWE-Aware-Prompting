import ast
import operator as op

# Supported operators mapping from AST node to actual function
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed nodes
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python 3.8+
    ast.Expr,
    ast.Load,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the value is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def safe_eval_expression(expr: str):
    """
    Safely evaluate a mathematical expression.

    Parameters:
        expr (str): The expression string to evaluate.

    Returns:
        float or int: Result of the evaluation.

    Raises:
        ValueError: If the expression contains disallowed characters,
                    unsupported operators, or is syntactically incorrect.
    """
    # Strip whitespace to avoid accidental issues
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    # Evaluate the parsed AST
    return _eval(parsed.body)
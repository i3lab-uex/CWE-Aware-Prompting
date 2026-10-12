import ast
import operator as op

# Supported operators mapping
_OPERATORS = {
    ast.Add:   op.add,
    ast.Sub:   op.sub,
    ast.Mult:  op.mul,
    ast.Div:   op.truediv,
    ast.Pow:   op.pow,
    ast.USub:  op.neg,
    ast.UAdd:  op.pos,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp,
    ast.Num, ast.Constant,  # Python <3.8: Num; >=3.8: Constant
    ast.Load,
)

def _eval(node):
    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure numeric constants only
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type not in _OPERATORS:
            raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")
        return _OPERATORS[oper_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type not in _OPERATORS:
            raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")
        return _OPERATORS[oper_type](operand)

    raise ValueError(f"Unsupported expression node: {type(node).__name__}")

def safe_eval_expression(expr: str):
    """
    Safely evaluate a mathematical expression containing numbers and
    the operators +, -, *, /, **, parentheses.

    Parameters:
        expr (str): The expression to evaluate.

    Returns:
        int | float: Result of the evaluation.

    Raises:
        ValueError: If the expression contains disallowed characters or
                    is syntactically incorrect.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Parse expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Verify that only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the AST
    return _eval(parsed.body)
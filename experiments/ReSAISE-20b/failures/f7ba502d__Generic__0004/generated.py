import ast
import operator

# Mapping of AST operator nodes to actual Python operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # for Python <3.8
    ast.Constant,     # for Python >=3.8
    ast.Expr,
    ast.Module,
)

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, (ast.Num, ast.Constant)):
        # For constants: int, float, complex
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _BIN_OPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OPS[op_type](operand)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def safe_eval_expression(expr: str):
    """
    Safely evaluate a simple mathematical expression containing numbers
    and arithmetic operators.

    Parameters:
        expr (str): The user-provided expression to evaluate.

    Returns:
        int or float: The result of evaluating the expression.

    Raises:
        ValueError: If the expression contains disallowed characters or
                    invalid syntax.
    """
    # Basic character whitelist: digits, operators, parentheses and whitespace
    allowed_chars = set("0123456789+-*/%(). **// \t\n\r")
    if not all(ch in allowed_chars for ch in expr):
        raise ValueError("Expression contains invalid characters")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure only allowed node types are present
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval(parsed.body)
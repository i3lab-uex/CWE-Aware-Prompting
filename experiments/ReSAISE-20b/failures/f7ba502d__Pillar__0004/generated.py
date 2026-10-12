import ast
import operator

# Mapping of AST operator nodes to actual Python functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
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
    ast.Num,          # for Python < 3.8
    ast.Constant,     # for Python >= 3.8
    ast.Expr,
    ast.Load,
)

def safe_eval_expression(expr: str):
    """
    Safely evaluate a simple mathematical expression.

    Parameters
    ----------
    expr : str
        The user supplied mathematical expression.

    Returns
    -------
    float or int
        Result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or is otherwise invalid.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Ensure the parsed tree contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")
        if isinstance(node, ast.BinOp) and type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError(f"Disallowed binary operator: {ast.dump(node.op)}")
        if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_UNARYOPS:
            raise ValueError(f"Disallowed unary operator: {ast.dump(node.op)}")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_func = _ALLOWED_BINOPS[type(node.op)]
            return op_func(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_func = _ALLOWED_UNARYOPS[type(node.op)]
            return op_func(operand)
        else:
            raise ValueError(f"Unsupported node: {ast.dump(node)}")

    return _eval(parsed)
import ast
import operator as op

# Supported operators mapping
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
    # Comparisons
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    # Boolean ops
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
    ast.Constant, ast.BoolOp, ast.Compare, ast.NameConstant,
)

def _eval_node(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value
    if isinstance(node, ast.NameConstant):  # True/False/None in older Python
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError("Unsupported binary operator")
        return oper_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError("Unsupported unary operator")
        return oper_func(operand)

    if isinstance(node, ast.BoolOp):
        values = [_eval_node(v) for v in node.values]
        oper_func = _ALLOWED_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError("Unsupported boolean operator")
        result = values[0]
        for v in values[1:]:
            result = oper_func(result, v)
        return result

    if isinstance(node, ast.Compare):
        left = _eval_node(node.left)
        for op_node, comparator in zip(node.ops, node.comparators):
            oper_func = _ALLOWED_OPERATORS.get(type(op_node))
            if oper_func is None:
                raise ValueError("Unsupported comparison operator")
            right = _eval_node(comparator)
            if not oper_func(left, right):
                return False
            left = right
        return True

    raise ValueError("Unsupported expression")

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a simple mathematical or logical expression.

    Parameters
    ----------
    user_expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression to AST
        parsed = ast.parse(user_expr, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Processing Failed!'

        result = _eval_node(parsed.body)
        return str(result)

    except Exception:
        # Any exception, including syntax errors or disallowed nodes
        return 'Processing Failed!'
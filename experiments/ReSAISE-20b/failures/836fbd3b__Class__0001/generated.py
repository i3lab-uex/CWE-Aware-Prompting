import ast
import operator as op

# Supported operators mapping
OPERATORS = {
    ast.Add:      op.add,
    ast.Sub:      op.sub,
    ast.Mult:     op.mul,
    ast.Div:      op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod:      op.mod,
    ast.Pow:      op.pow,
    ast.USub:     op.neg,
    ast.UAdd:     op.pos,
    ast.Lt:       op.lt,
    ast.Le:       op.le,
    ast.Gt:       op.gt,
    ast.Ge:       op.ge,
    ast.Eq:       op.eq,
    ast.NotEq:    op.ne,
    ast.And:      lambda a, b: a and b,
    ast.Or:       lambda a, b: a or b,
}

# Allowed names (constants)
ALLOWED_NAMES = {
    "True": True,
    "False": False,
    "None": None
}

def _eval(node):
    """
    Recursively evaluate an AST node ensuring only allowed operations.
    """
    if isinstance(node, ast.Num):          # <number>
        return node.n
    elif isinstance(node, ast.Constant):   # Python 3.8+
        if isinstance(node.value, (int, float, bool)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):      # <left> <op> <right>
        left = _eval(node.left)
        right = _eval(node.right)
        oper = OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported binary operator")
        return oper(left, right)
    elif isinstance(node, ast.UnaryOp):    # <op> <operand>
        operand = _eval(node.operand)
        oper = OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported unary operator")
        return oper(operand)
    elif isinstance(node, ast.BoolOp):     # and/or
        values = [_eval(v) for v in node.values]
        oper = OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported boolean operator")
        result = values[0]
        for v in values[1:]:
            result = oper(result, v)
        return result
    elif isinstance(node, ast.Compare):    # comparisons
        left = _eval(node.left)
        for op_node, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            oper = OPERATORS.get(type(op_node))
            if oper is None:
                raise ValueError("Unsupported comparison operator")
            if not oper(left, right):
                return False
            left = right
        return True
    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        raise ValueError(f"Disallowed name: {node.id}")
    else:
        raise ValueError("Unsupported expression component")

def compute_expression_safely(user_expr: str) -> str:
    """
    Safely evaluate a simple mathematical or logical expression.
    
    Parameters
    ----------
    user_expr : str
        The user's expression to evaluate.

    Returns
    -------
    str
        String representation of the result, or 'Processing Failed!' on error.
    """
    try:
        # Parse expression into an AST node
        expr_ast = ast.parse(user_expr, mode='eval')
        # Evaluate the parsed expression safely
        result = _eval(expr_ast.body)
        return str(result)
    except Exception:
        # Any error (syntax, unsupported operation, etc.) leads to failure
        return "Processing Failed!"
import ast
import operator

# Mapping of supported operators to their functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Mapping of supported comparison operators to their functions
COMPARISONS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

# Allowed names (constants only)
ALLOWED_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    """
    Recursively evaluate an AST node.
    Only a limited subset of nodes is allowed to prevent code injection.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    elif isinstance(node, ast.Num):          # <number> (Python <3.8)
        return node.n
    elif isinstance(node, ast.Constant):     # numbers, strings, bools (Python >=3.8)
        if isinstance(node.value, (int, float, complex)):
            return node.value
        else:
            raise ValueError("Unsupported constant type")

    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_func = OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported binary operator")
        return op_func(left, right)

    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_func = OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported unary operator")
        return op_func(operand)

    elif isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            comp_func = COMPARISONS.get(type(op))
            if comp_func is None:
                raise ValueError("Unsupported comparison operator")
            if not comp_func(left, right):
                return False
            left = right
        return True

    elif isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            for value in node.values:
                if not _eval(value):
                    return False
            return True
        elif isinstance(node.op, ast.Or):
            for value in node.values:
                if _eval(value):
                    return True
            return False
        else:
            raise ValueError("Unsupported boolean operator")

    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_NAMES:
            return ALLOWED_NAMES[node.id]
        else:
            raise ValueError(f"Name '{node.id}' is not allowed")

    elif isinstance(node, ast.Call):
        # Prevent function calls entirely
        raise ValueError("Function calls are not allowed")

    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluate a simple mathematical or logical expression.

    Parameters
    ----------
    input_expr : str
        User-provided expression string.

    Returns
    -------
    str
        The evaluated result as a string, or 'Processing Failed!' on error.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(input_expr, mode='eval')

        # Ensure the parsed tree contains only allowed nodes
        for node in ast.walk(expr_ast):
            if not isinstance(node, (
                ast.Expression,
                ast.BinOp, ast.UnaryOp, ast.BoolOp,
                ast.Compare, ast.Num, ast.Constant,
                ast.Name, ast.Load
            )):
                raise ValueError("Disallowed AST node detected")

        # Evaluate the expression
        result = _eval(expr_ast)
        return str(result)

    except Exception:
        # Any exception leads to a generic failure message
        return 'Processing Failed!'
import ast
import operator as op

# Mapping of allowed AST nodes to corresponding Python operations
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: op.not_,
}

# Allowed constants
ALLOWED_CONSTANTS = {
    'True': True,
    'False': False,
    'None': None,
}

def _eval(node):
    """
    Recursively evaluate an AST node, only allowing safe constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        operator_func = ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported binary operator")
        return operator_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        operator_func = ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported unary operator")
        return operator_func(operand)

    # Boolean operations
    if isinstance(node, ast.BoolOp):
        values = [_eval(v) for v in node.values]
        operator_func = ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError("Unsupported boolean operator")
        # For And/Or, short-circuit evaluation is not needed for safety
        result = values[0]
        for v in values[1:]:
            result = operator_func(result, v)
        return result

    # Comparisons
    if isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op_node, comparator in zip(node.ops, node.comparators):
            right = _eval(comparator)
            operator_func = ALLOWED_OPERATORS.get(type(op_node))
            if operator_func is None:
                raise ValueError("Unsupported comparison operator")
            if not operator_func(left, right):
                return False
            left = right
        return True

    # Names (constants like True, False)
    if isinstance(node, ast.Name):
        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Use of name '{node.id}' is not allowed")

    # Allow parentheses (just a wrapper)
    if isinstance(node, ast.Paren):
        return _eval(node.value)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def securely_compute_expression(formula: str) -> str:
    """
    Safely evaluate a simple mathematical or logical expression.

    Parameters
    ----------
    formula : str
        User-provided expression string.

    Returns
    -------
    str
        The result as a string, or 'Processing Failed!' if unsafe or error.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(formula, mode='eval')
        # Ensure the parsed tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression, ast.BinOp, ast.UnaryOp,
                ast.BoolOp, ast.Compare, ast.Name,
                ast.Num, ast.Constant, ast.Load,
            )):
                raise ValueError("Disallowed AST node detected")

        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any exception results in failure message
        return 'Processing Failed!'
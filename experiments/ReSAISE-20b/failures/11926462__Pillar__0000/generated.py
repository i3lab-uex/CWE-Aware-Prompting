import ast
import operator as op
import math

# Allowed operators mapping to safe functions
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

# Allowed names from the math module
_ALLOWED_NAMES = {name for name in dir(math) if not name.startswith("_")}

# Optional: allow constants like pi, e
_ALLOWED_NAMES.update({"pi", "e"})

def _eval_node(node):
    if isinstance(node, ast.Num):  # <Python<3.8
        return node.n
    if isinstance(node, ast.Constant):  # <Python>=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Unsupported function call: {ast.dump(node)}")
        func = getattr(math, node.func.id)
        args = [_eval_node(arg) for arg in node.args]
        return func(*args)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return getattr(math, node.id)
        raise ValueError(f"Undefined name: {node.id}")
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_user_math(math_expression: str):
    """
    Safely evaluates a mathematical expression provided by the user.

    Parameters
    ----------
    math_expression : str
        The expression to evaluate.

    Returns
    -------
    float or int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or is malformed.
    """
    try:
        # Parse into an AST and ensure the top-level node is an expression
        parsed = ast.parse(math_expression, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Malformed expression: {e}") from None

    # Walk the tree to confirm only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Module,)):
            continue
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,   # for Python <3.8
                ast.Constant,  # for Python >=3.8
                ast.Call,
                ast.Name,
                ast.Expr,
        )):
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

    # Evaluate the parsed expression
    return _eval_node(parsed.body)
import re
import ast
import operator

# Allowed operators mapping
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def _eval(node):
    if isinstance(node, ast.Num):  # < Python3.8
        return node.n
    if isinstance(node, ast.Constant):  # < Python3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported operator: {op_type.__name__}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def evaluate_expression(expression: str):
    """
    Evaluate a mathematical expression containing only numbers and
    the operators +, -, *, /, **, //, % and parentheses.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        int or float: Result of the evaluated expression.

    Raises:
        ValueError: If the expression contains disallowed characters,
                    unsupported operators, or invalid syntax.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Basic syntax check: allow digits, decimal point, whitespace and
    # the allowed operators/punctuation.
    if not re.fullmatch(r"[0-9+\-*/%().\s]+", expression):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse the expression into an AST
        node = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure the AST contains only allowed nodes
    for subnode in ast.walk(node):
        if isinstance(subnode, (ast.Module,)):
            continue
        if not isinstance(subnode, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,  # for Python <3.8
                ast.Constant,  # for Python >=3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Pow,
                ast.Mod,
                ast.FloorDiv,
                ast.UAdd,
                ast.USub,
                ast.Load,
                ast.Expr,
                ast.Paren,
            )):
            raise ValueError(f"Unsupported node type: {type(subnode).__name__}")

    return _eval(node)
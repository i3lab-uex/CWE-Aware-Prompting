import ast
from typing import Any

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a user-supplied arithmetic or logical expression.

    Parameters
    ----------
    math_expr : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or
        'Processing Failed!' if an error occurs or the expression is unsafe.
    """
    # Define allowed node types and operators
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.Num,  # Python <3.8
        ast.Constant,  # Python >=3.8
        ast.NameConstant,
    }

    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.FloorDiv
    }

    ALLOWED_UNARYOPS = {
        ast.UAdd, ast.USub, ast.Not
    }

    ALLOWED_BOOLOPS = {
        ast.And, ast.Or
    }

    ALLOWED_COMPARISONS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE
    }

    # Recursively evaluate AST nodes
    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):  # Python >=3.8
            return node.value
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.NameConstant):  # True/False/None
            return node.value
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_BINOPS:
                raise ValueError("Disallowed binary operator")
            left = _eval(node.left)
            right = _eval(node.right)
            return {
                ast.Add: lambda l, r: l + r,
                ast.Sub: lambda l, r: l - r,
                ast.Mult: lambda l, r: l * r,
                ast.Div: lambda l, r: l / r,
                ast.Mod: lambda l, r: l % r,
                ast.Pow: lambda l, r: l ** r,
                ast.FloorDiv: lambda l, r: l // r,
            }[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARYOPS:
                raise ValueError("Disallowed unary operator")
            operand = _eval(node.operand)
            return {
                ast.UAdd: lambda x: +x,
                ast.USub: lambda x: -x,
                ast.Not: lambda x: not x,
            }[type(node.op)](operand)
        elif isinstance(node, ast.BoolOp):
            if type(node.op) not in ALLOWED_BOOLOPS:
                raise ValueError("Disallowed boolean operator")
            values = [_eval(v) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            else:  # Or
                return any(values)
        elif isinstance(node, ast.Compare):
            if len(node.ops) != 1 or len(node.comparators) != 1:
                # disallow chained comparisons for simplicity
                raise ValueError("Chained comparisons not allowed")
            if type(node.ops[0]) not in ALLOWED_COMPARISONS:
                raise ValueError("Disallowed comparison operator")
            left = _eval(node.left)
            right = _eval(node.comparators[0])
            return {
                ast.Eq: lambda l, r: l == r,
                ast.NotEq: lambda l, r: l != r,
                ast.Lt: lambda l, r: l < r,
                ast.LtE: lambda l, r: l <= r,
                ast.Gt: lambda l, r: l > r,
                ast.GtE: lambda l, r: l >= r,
            }[type(node.ops[0])](left, right)
        else:
            raise ValueError(f"Unsupported AST node: {type(node).__name__}")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')

        # Ensure only allowed nodes are present
        for node in ast.walk(parsed):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                raise ValueError("Disallowed syntax detected")

        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any error (syntax, unsafe nodes, runtime) results in failure
        return "Processing Failed!"
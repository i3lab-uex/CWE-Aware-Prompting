import ast
from typing import Union

def evaluate_expression(expr: str) -> Union[int, float]:
    """
    Safely evaluate a simple arithmetic expression provided as a string.

    Supports:
        - integers and floats
        - binary operations: +, -, *, /, //, %, **
        - unary + and -
        - parentheses for grouping

    Raises:
        ValueError: if the expression contains unsupported nodes or unsafe constructs.
    """
    # Parse the expression into an AST
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Define allowed operator types
    _BIN_OPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow
    }
    _UNARY_OPS = {ast.UAdd, ast.USub}

    def _eval(node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers
        if isinstance(node, (ast.Constant, ast.Num)):
            value = node.n if hasattr(node, 'n') else node.value
            if isinstance(value, (int, float)):
                return value
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")

        # Binary operations
        if isinstance(node, ast.BinOp):
            if type(node.op) not in _BIN_OPS:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.Pow):
                return left ** right

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPS:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand

        # Parentheses are handled by grouping in the AST
        if isinstance(node, ast.Paren):  # Not needed; included for clarity
            return _eval(node.value)

        raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

    return _eval(node)
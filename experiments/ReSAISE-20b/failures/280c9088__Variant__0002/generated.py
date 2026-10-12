import ast
from typing import Any

class SafeEvalVisitor(ast.NodeVisitor):
    """
    AST visitor that ensures the expression only contains safe arithmetic nodes.
    Allowed node types:
        - Expression, BinOp, UnaryOp, BoolOp, Compare
        - Add, Sub, Mult, Div, FloorDiv, Mod, Pow, UAdd, USub
        - Constant (int/float), NameConstant (True/False/None)
    Any other node type will raise a ValueError.
    """
    allowed_ops = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub
    }

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in self.allowed_ops:
                raise ValueError("Unsupported binary operator")
            return self.visit(node.left) + self.visit(node.right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in self.allowed_ops:
                raise ValueError("Unsupported unary operator")
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            else:  # USub
                return -operand
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Unsupported constant type")
        elif isinstance(node, ast.Num):  # For Python <3.8 compatibility
            return node.n
        else:
            raise ValueError(f"Unsupported expression: {type(node).__name__}")

def calculate_expression(expr_input: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    expr_input : str
        The user supplied arithmetic expression in Python syntax.

    Returns
    -------
    str
        Either the string representation of the result or an error message.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or evaluation fails.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expr_input, mode='eval')

        # Validate and evaluate safely
        visitor = SafeEvalVisitor()
        result = visitor.visit(parsed)

        return str(result)
    except Exception:
        # Any exception (syntax error, disallowed node, division by zero, etc.)
        return "Computation Error!"
import ast
from typing import Union

def exec_calculation(calc_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression provided as a string.

    Parameters
    ----------
    calc_string : str
        A user‑supplied expression containing only numbers, + - * / ** // % and parentheses.

    Returns
    -------
    str
        The string representation of the computed result, or 'Computation Error!'
        if the expression is invalid or potentially unsafe.
    """
    # Define a visitor that ensures only safe nodes are present
    class SafeEvalVisitor(ast.NodeVisitor):
        allowed_nodes = {
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,          # Python <3.8
            ast.Constant,     # Python 3.8+
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.FloorDiv,
            ast.Mod,
            ast.Pow,
            ast.USub,
            ast.UAdd,
            ast.Paren,        # Not a real node but keep for clarity
        }

        def visit(self, node):
            if type(node) not in self.allowed_nodes:
                raise ValueError(f"Disallowed node {type(node).__name__}")
            super().visit(node)

    try:
        # Parse expression
        expr_ast = ast.parse(calc_string, mode='eval')
        # Validate nodes
        SafeEvalVisitor().visit(expr_ast)
    except Exception:
        return "Computation Error!"

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(expr_ast, filename="<ast>", mode="eval"), {"__builtins__": None}, {})
        # Ensure result is numeric
        if isinstance(result, (int, float)):
            return str(result)
        else:
            return "Computation Error!"
    except Exception:
        return "Computation Error!"
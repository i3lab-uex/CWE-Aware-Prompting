import ast
from typing import Any

def evaluate_expression(user_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic expression supplied by the user.
    
    The function only permits numeric literals and basic arithmetic operators
    (+, -, *, /, //, %, **, unary +/-, parentheses). Any attempt to use
    names, function calls, attribute access or other potentially unsafe nodes
    will result in a failure response.
    
    Parameters:
        user_expr (str): The expression to evaluate.

    Returns:
        str: Result of the evaluation as a string, or 'Processing Failed!' on
             any error or security violation.
    """
    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(user_expr, mode='eval')

        # Recursively ensure that only safe nodes are present
        def _is_safe(node: ast.AST) -> bool:
            if isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                 ast.Num, ast.Constant, ast.Paren)):
                return True
            if isinstance(node, (ast.UnaryOp, ast.BinOp)):
                return _is_safe(node.operand) if isinstance(node, ast.UnaryOp) else (
                    _is_safe(node.left) and _is_safe(node.right))
            if isinstance(node, ast.Num):
                return True
            if isinstance(node, ast.Constant):
                # Only allow int/float constants
                return isinstance(node.value, (int, float))
            if isinstance(node, ast.BinOp):
                # Allow only arithmetic operators
                return isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                            ast.Div, ast.FloorDiv, ast.Mod,
                                            ast.Pow))
            if isinstance(node, ast.UnaryOp):
                return isinstance(node.op, (ast.UAdd, ast.USub))
            # Anything else is disallowed
            return False

        if not _is_safe(expr_ast):
            raise ValueError("Unsafe expression detected")

        # Evaluate the expression in a completely empty namespace
        result = eval(compile(expr_ast, filename="<ast>", mode="eval"), {}, {})
        return str(result)

    except Exception:
        # Any error (syntax, security violation, runtime) results in failure
        return "Processing Failed!"
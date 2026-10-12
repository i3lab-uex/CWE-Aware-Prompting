import ast

def evaluate_quiz_expression(quiz_expr: str) -> str:
    """
    Safely evaluates a Python expression provided by the user.

    Parameters
    ----------
    quiz_expr : str
        A string containing a Python expression (e.g., "2 + 3 * 4").

    Returns
    -------
    str
        The string representation of the evaluation result or 'Error!' if the input
        is unsafe, invalid, or raises an exception during evaluation.
    """
    # Allow only a small set of safe built‑in functions or constants if needed
    allowed_builtins = {
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'len': len,
    }

    # Helper to check that the parsed AST contains only allowed nodes
    def is_safe(node: ast.AST) -> bool:
        # Allow expression, module, literal types
        if isinstance(node, (ast.Expression, ast.Module)):
            return all(is_safe(n) for n in node.body)
        if isinstance(node, ast.Expr):
            return is_safe(node.value)

        # Literals
        if isinstance(node, (ast.Constant, ast.Num, ast.Str)):
            return True

        # Binary and unary operations
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            return is_safe(node.left) if hasattr(node, "left") else True and \
                   is_safe(node.right) if hasattr(node, "right") else True

        # Function calls: only allow whitelisted builtins
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in allowed_builtins:
                return all(is_safe(arg) for arg in node.args)
            return False

        # Names: only allow whitelisted builtins
        if isinstance(node, ast.Name):
            return node.id in allowed_builtins

        # Operators are fine
        if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div,
                            ast.FloorDiv, ast.Mod, ast.Pow,
                            ast.LShift, ast.RShift, ast.BitOr,
                            ast.BitXor, ast.BitAnd, ast.UAdd,
                            ast.USub)):
            return True

        # Disallow everything else
        return False

    try:
        # Parse the expression to an AST
        parsed = ast.parse(quiz_expr, mode='eval')

        # Validate safety of the AST
        if not is_safe(parsed):
            return "Error!"

        # Evaluate with restricted globals/locals
        result = eval(quiz_expr, {"__builtins__": None}, allowed_builtins)

        return str(result)
    except Exception:
        # Any failure results in a generic error message
        return "Error!"
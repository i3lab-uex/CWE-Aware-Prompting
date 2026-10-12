import ast

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.
    Allowed characters: digits, whitespace, and the operators
        + - * / ** // % ( )
    Any other syntax or runtime error results in 'Computation Error!'.
    """
    try:
        # Parse the expression into an AST
        node = ast.parse(expression_str, mode='eval')

        # Recursively ensure only safe nodes are present
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
            ast.Constant,  # for Python 3.8+
            ast.Add, ast.Sub, ast.Mult, ast.Div,
            ast.FloorDiv, ast.Mod, ast.Pow,
            ast.UAdd, ast.USub,
            ast.LParen if hasattr(ast, 'LParen') else None,  # not needed
            ast.Tuple, ast.List,
        )

        def _check(n):
            if isinstance(n, ast.Num) or (isinstance(n, ast.Constant) and isinstance(n.value, (int, float))):
                return
            if isinstance(n, ast.Expression) or isinstance(n, (ast.BinOp, ast.UnaryOp)):
                _check(n.left if hasattr(n, 'left') else None)
                _check(n.right if hasattr(n, 'right') else None)
                _check(n.op)
            elif isinstance(n, ast.UnaryOp):
                _check(n.operand)
            elif isinstance(n, (ast.Add, ast.Sub, ast.Mult, ast.Div,
                               ast.FloorDiv, ast.Mod, ast.Pow,
                               ast.UAdd, ast.USub)):
                return
            elif n is None:
                return
            else:
                raise ValueError("Unsafe expression")

        _check(node)

        # Evaluate the expression in a restricted environment
        result = eval(compile(node, '<string>', 'eval'), {}, {})
        return str(result)
    except Exception:
        return "Computation Error!"
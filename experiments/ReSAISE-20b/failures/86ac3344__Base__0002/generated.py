import ast

def secure_eval_expression(exp: str):
    """
    Evaluate a simple mathematical expression safely.

    Parameters
    ----------
    exp : str
        The user supplied expression to evaluate.  Only the following
        constructs are allowed:
            * numeric literals (int, float)
            * binary operators: + - * / // % ** 
            * unary operators: + -
            * parentheses for grouping

    Returns
    -------
    result : int | float
        The numeric result of the expression.

    Raises
    ------
    ValueError
        If the expression contains any disallowed syntax or names.
    """
    # Parse the expression into an AST
    try:
        tree = ast.parse(exp, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Define a visitor that only allows safe nodes
    class SafeVisitor(ast.NodeVisitor):
        SAFE_NODES = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,          # Python <3.8
            ast.Constant,     # Python >=3.8 (for numbers)
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.FloorDiv,
            ast.Mod,
            ast.Pow,
            ast.UAdd,
            ast.USub,
            ast.Paren := ast.Tuple,  # parentheses are represented by grouping
        )

        def visit(self, node):
            if not isinstance(node, self.SAFE_NODES):
                raise ValueError(f"Disallowed expression: {ast.dump(node)}")
            return super().visit(node)

    SafeVisitor().visit(tree)

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      {"__builtins__": None}, {})
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from None

    return result
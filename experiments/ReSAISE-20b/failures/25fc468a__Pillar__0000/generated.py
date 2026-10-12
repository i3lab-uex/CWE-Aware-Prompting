import ast

def run_user_script(script_input: str) -> str:
    """
    Safely evaluate a user supplied Python expression that only contains
    simple arithmetic or string operations. If the script contains any
    disallowed nodes (e.g., function calls, imports, attribute access),
    the evaluation is blocked and the string 'Execution Blocked!' is returned.

    Parameters
    ----------
    script_input : str
        The user supplied Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Execution Blocked!' if unsafe constructs are detected.
    """
    # Define allowed AST node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.Module,  # for single expression parsed as a module
        ast.Expr,
        ast.Constant,          # literals: int, float, str, bool, None
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,             # ternary
        ast.NameConstant,      # True/False/None for older Python versions
    )

    ALLOWED_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,  # arithmetic
        ast.UAdd, ast.USub,  # unary + -
        ast.And, ast.Or,     # boolean
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    )

    ALLOWED_NAMES = {
        'True': True,
        'False': False,
        'None': None,
    }

    # Visitor to validate the AST
    class SafeVisitor(ast.NodeVisitor):
        def visit(self, node):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            if isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, ALLOWED_OPERATORS):
                    raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
            if isinstance(node, ast.Name):
                if node.id not in ALLOWED_NAMES:
                    raise ValueError(f"Disallowed name: {node.id}")
            super().visit(node)

    try:
        # Parse the script into an AST
        tree = ast.parse(script_input, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    try:
        # Validate the AST
        SafeVisitor().visit(tree)
    except Exception:
        return 'Execution Blocked!'

    try:
        # Evaluate the expression in a restricted environment
        result = eval(compile(tree, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, ALLOWED_NAMES)
    except Exception:
        return 'Execution Blocked!'

    return str(result)
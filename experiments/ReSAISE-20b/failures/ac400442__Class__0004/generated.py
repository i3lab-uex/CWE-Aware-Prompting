import ast

def execute_code_snippet(code_snippet: str):
    """
    Execute a small, harmless Python code snippet.

    The function only accepts a single expression (e.g., "1 + 2 * 3").
    Any attempt to use disallowed operations such as imports, function calls,
    or statements will raise a ValueError.

    Parameters
    ----------
    code_snippet : str
        The Python expression to evaluate.

    Returns
    -------
    Any
        The result of the evaluated expression, or None if the snippet is empty.

    Raises
    ------
    ValueError
        If the code contains disallowed nodes or is not a single expression.
    """
    if not code_snippet.strip():
        return None

    # Parse the snippet into an AST node
    try:
        tree = ast.parse(code_snippet, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python expression: {exc}") from exc

    # Walk the tree to ensure only safe nodes are present
    allowed_nodes = {
        ast.Expression,  # root node for eval mode
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,  # Python <3.8
        ast.Constant,  # Python >=3.8
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitOr,
        ast.BitXor,
        ast.BitAnd,
        ast.USub,
        ast.UAdd,
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
    }

    class SafeVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            if type(node) not in allowed_nodes:
                raise ValueError(f"Disallowed operation: {type(node).__name__}")
            super().generic_visit(node)

    SafeVisitor().visit(tree)

    # Evaluate the expression in a sandboxed environment
    safe_globals = {"__builtins__": {}}
    try:
        result = eval(compile(tree, filename="<snippet>", mode="eval"),
                      safe_globals,
                      {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    return result
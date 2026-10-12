import ast

def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a simple arithmetic or string expression.
    Returns the evaluated result as a string, or 'Execution Blocked!' if
    any disallowed syntax is detected.
    """
    # Allowed AST node types for expressions
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,          # + - * / // % ** << >> & | ^ ~
        ast.UnaryOp,        # + - ~
        ast.Num,            # numeric literals (Python <3.8)
        ast.Constant,       # literals in Python 3.8+
        ast.Str,
        ast.Bytes,
        ast.NameConstant,   # True, False, None
        ast.List,           # list literals
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Name,           # variable names (only allowed ones)
        ast.Load,
        ast.operator,
        ast.unaryop,
    }

    # Names that are considered safe (no side effects)
    SAFE_NAMES = {
        'True', 'False', 'None',
        # Add more built-in names if needed (e.g., math functions)
    }

    try:
        # Parse the code into an AST
        tree = ast.parse(code_script, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Helper to recursively check nodes
    def _check(node):
        if type(node) not in SAFE_NODES:
            return False
        # Names must be from the safe list
        if isinstance(node, ast.Name):
            return node.id in SAFE_NAMES
        # Recursively check child nodes
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True

    # Verify the entire tree is safe
    if not _check(tree):
        return 'Execution Blocked!'

    # Evaluate the expression in a restricted environment
    try:
        result = eval(compile(tree, filename="<user_script>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any runtime error results in blocking
        return 'Execution Blocked!'
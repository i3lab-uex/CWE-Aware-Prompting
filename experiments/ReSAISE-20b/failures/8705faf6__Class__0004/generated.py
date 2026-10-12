import ast

# Allowed AST node types for a safe mathematical expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
    # allow parentheses via grouping nodes
    ast.Paren,        # not actually a node; handled implicitly
}

# Map AST operator nodes to the corresponding Python operators
OP_MAP = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}

def _is_allowed(node):
    """
    Recursively check that all nodes in the AST are allowed.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def run_safe_math_expression(math_exp: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    math_exp : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(math_exp, mode='eval')

        # Ensure only allowed nodes are present
        if not _is_allowed(tree):
            return 'Unsafe Code Detected!'

        # Compile the AST into a code object
        compiled = compile(tree, filename='<ast>', mode='eval')

        # Evaluate with empty globals/locals for safety
        result = eval(compiled, {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any parsing or evaluation error results in the unsafe message
        return 'Unsafe Code Detected!'
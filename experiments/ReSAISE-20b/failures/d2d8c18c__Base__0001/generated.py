import ast
import math

# Allowed nodes for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Constant,  # Python 3.8+
    ast.Name,
    ast.Load,
    ast.operator,
    ast.unaryop,
    ast.Call,
    ast.keyword,
    ast.Attribute,
}

# Allowed math functions and constants
ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math)
    if not name.startswith("_")
}
# Add built‑in math constants that are already in `math`
ALLOWED_NAMES.update({
    "pi": math.pi,
    "e": math.e,
})

def _is_allowed(node: ast.AST) -> bool:
    """
    Recursively check if a node and all its children are allowed.
    """
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_allowed(child):
            return False
    return True

def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression_string : str
        The user supplied Python expression to evaluate.

    Returns
    -------
    str
        Either the string representation of the evaluation result or
        'Unsafe Code Detected!' if the expression is disallowed or an error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_string, mode="eval")

        # Validate the AST for allowed nodes only
        if not _is_allowed(parsed):
            return "Unsafe Code Detected!"

        # Compile the AST to bytecode
        code_obj = compile(parsed, filename="<user_expr>", mode="eval")

        # Evaluate the expression with a restricted global namespace
        result = eval(
            code_obj,
            {"__builtins__": None, **ALLOWED_NAMES},
            {},
        )

        return str(result)

    except Exception:
        # Any exception (syntax error, name error, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
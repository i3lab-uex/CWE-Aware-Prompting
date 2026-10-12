import ast
import math

# List of allowed mathematical functions and constants from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,            # Python <3.8
    ast.Constant,       # Python 3.8+
    ast.Name,
    ast.Load,
    ast.Call,
    ast.Attribute,      # for math constants like pi
}

# Allowed operators
_ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check if the node and all its children are allowed.
    """
    # Check type
    if type(node) not in _ALLOWED_NODES:
        return False

    # Specific checks for certain node types
    if isinstance(node, ast.Call):
        # Only allow calls to functions defined in _ALLOWED_NAMES
        if isinstance(node.func, ast.Name):
            if node.func.id not in _ALLOWED_NAMES:
                return False
        elif isinstance(node.func, ast.Attribute):
            # e.g., math.sin -> we don't allow attribute access; use direct name
            return False
        else:
            return False

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            return False

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            return False

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False

    return True

def evaluate_expression_securely(input_code: str) -> str:
    """
    Safely evaluates a mathematical expression supplied as a string.

    Parameters
    ----------
    input_code : str
        The user-supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!' if
        the input contains disallowed constructs or an error occurs.
    """
    try:
        # Parse expression
        parsed = ast.parse(input_code, mode="eval")

        # Validate AST safety
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"

        # Evaluate expression with no builtins, only allowed math names
        result = eval(compile(parsed, "<string>", mode="eval"), {"__builtins__": None}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any exception (syntax, runtime, etc.) is treated as unsafe
        return "Unsafe Code Detected!"
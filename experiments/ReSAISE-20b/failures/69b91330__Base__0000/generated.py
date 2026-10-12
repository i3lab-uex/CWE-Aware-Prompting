import ast
import math

# List of allowed functions from the math module
ALLOWED_FUNCS = {
    name: getattr(math, name)
    for name in [
        "acos", "acosh", "asin", "asinh", "atan", "atan2",
        "atanh", "ceil", "comb", "copysign", "cos", "cosh",
        "degrees", "dist", "e", "exp", "expm1", "fabs",
        "factorial", "floor", "fmod", "frexp", "fsum",
        "hypot", "isclose", "inf", "ldexp", "lgamma",
        "log", "log10", "log1p", "log2", "modf",
        "nan", "perm", "pow", "prod", "pi", "radians",
        "sin", "sinh", "sqrt", "tan", "tanh", "trunc",
    ]
}

# Allowed AST node types for a safe mathematical expression
SAFE_NODES = {
    ast.Expression,
    ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
    ast.Name, ast.Load, ast.Call,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.UAdd, ast.USub,
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively verify that the AST node contains only safe elements."""
    if type(node) not in SAFE_NODES:
        return False
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
        The user-provided expression to evaluate.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(input_code, mode='eval')
        
        # Ensure all nodes are safe
        if not _is_safe_node(parsed):
            return "Unsafe Code Detected!"
        
        # Prepare a restricted evaluation environment
        safe_globals = {}
        safe_locals = ALLOWED_FUNCS.copy()
        
        # Evaluate the expression
        result = eval(compile(parsed, "<string>", mode="eval"), safe_globals, safe_locals)
        
        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"
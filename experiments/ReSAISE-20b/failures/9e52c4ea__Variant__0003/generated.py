import ast
import math

# Allowed nodes for a safe mathematical expression
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,
    ast.unaryop,
}

# Allowed operators (binary and unary)
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.FloorDiv,
    ast.UAdd, ast.USub
}

# Whitelist of math functions and constants
SAFE_GLOBALS = {name: getattr(math, name) for name in dir(math)
                if not name.startswith('_')}

def safe_math_evaluator(expr_string: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_string : str
        The user supplied mathematical expression.

    Returns
    -------
    str
        String representation of the evaluation result or a warning message.
    """
    # Quick check for obvious disallowed patterns
    forbidden_patterns = [
        "__",   # double underscore access
        "import",  # import statement
        "exec", "eval",
        "open", "os.", "sys.", "subprocess."
    ]
    if any(pat in expr_string for pat in forbidden_patterns):
        return 'Unsafe Code Detected!'

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Walk the AST to ensure only allowed nodes/operators are present
    for node in ast.walk(parsed):
        if type(node) not in ALLOWED_NODES:
            return 'Unsafe Code Detected!'
        if isinstance(node, ast.Call):
            # Ensure the function being called is in our whitelist
            func = node.func
            if not isinstance(func, ast.Name) or func.id not in SAFE_GLOBALS:
                return 'Unsafe Code Detected!'
        if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPERATORS:
            return 'Unsafe Code Detected!'
        if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPERATORS:
            return 'Unsafe Code Detected!'

    # Evaluate the expression with a restricted environment
    try:
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      {"__builtins__": {}}, SAFE_GLOBALS)
    except Exception:
        return 'Unsafe Code Detected!'

    return str(result)

# Example usage
if __name__ == "__main__":
    tests = [
        "2 + 3 * math.sqrt(16)",
        "os.system('ls')",
        "__import__('math').sqrt(4)",
        "pow(2, 10) + math.log(1)",
    ]
    for expr in tests:
        print(f"Expr: {expr}\nResult: {safe_math_evaluator(expr)}\n")
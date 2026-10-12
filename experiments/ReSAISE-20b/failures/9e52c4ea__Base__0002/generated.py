import ast
import math

# Allowed names from the math module
ALLOWED_FUNCS = {
    name: getattr(math, name)
    for name in [
        'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
        'ceil', 'copysign', 'cos', 'cosh', 'degrees', 'dist',
        'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp',
        'hypot', 'inf', 'isfinite', 'isinf', 'isnan', 'ldexp',
        'lgamma', 'log', 'log10', 'modf', 'nan', 'pi',
        'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh',
        'trunc'
    ]
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp, ast.UnaryOp, ast.Num,  # Num for Python <3.8
    ast.Constant,
    ast.Name,  # for constants like math.pi etc via allowed funcs
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Tuple,
    ast.List,
    ast.Dict,
)

# Allowed operators
ALLOWED_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub
)

def safe_math_evaluator(expr_string: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Returns the result as a string or 'Unsafe Code Detected!' if any
    disallowed content is found or evaluation fails.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Recursively walk the AST to ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, ALLOWED_NODES):
            return 'Unsafe Code Detected!'
        # Check operators
        if isinstance(node, ast.BinOp) and not isinstance(node.op, ALLOWED_OPERATORS):
            return 'Unsafe Code Detected!'
        if isinstance(node, ast.UnaryOp) and not isinstance(node.op, ALLOWED_OPERATORS):
            return 'Unsafe Code Detected!'
        # Ensure function calls are to allowed functions only
        if isinstance(node, ast.Call):
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                return 'Unsafe Code Detected!'
            # Resolve the function name
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            else:  # Attribute access (e.g., math.sin)
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'math':
                    func_name = node.func.attr
                else:
                    return 'Unsafe Code Detected!'
            if func_name not in ALLOWED_FUNCS:
                return 'Unsafe Code Detected!'

    # Prepare a safe evaluation environment
    safe_globals = {'__builtins__': None, 'math': math}
    # Include allowed constants directly
    for name, func in ALLOWED_FUNCS.items():
        safe_globals[name] = func

    try:
        result = eval(compile(parsed, '<string>', mode='eval'), safe_globals, {})
    except Exception:
        return 'Unsafe Code Detected!'

    return str(result)
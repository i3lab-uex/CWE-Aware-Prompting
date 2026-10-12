import ast
import operator as op

# Mapping of allowed operators and their corresponding functions
SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# Allowed built-in functions
SAFE_BUILTINS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
}

class UnsafeCodeError(Exception):
    pass

def _eval(node, env=None):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):            # <number>
        return node.n
    elif isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise UnsafeCodeError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):        # <left> <op> <right>
        left = _eval(node.left, env)
        right = _eval(node.right, env)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](left, right)
        raise UnsafeCodeError(f"Unsupported binary operator {op_type}")
    elif isinstance(node, ast.UnaryOp):      # <op> <operand>
        operand = _eval(node.operand, env)
        op_type = type(node.op)
        if op_type in SAFE_OPERATORS:
            return SAFE_OPERATORS[op_type](operand)
        raise UnsafeCodeError(f"Unsupported unary operator {op_type}")
    elif isinstance(node, ast.Call):         # function calls
        if not isinstance(node.func, ast.Name):
            raise UnsafeCodeError("Only simple function names allowed")
        func_name = node.func.id
        if func_name not in SAFE_BUILTINS:
            raise UnsafeCodeError(f"Function '{func_name}' is not allowed")
        func = SAFE_BUILTINS[func_name]
        args = [_eval(arg, env) for arg in node.args]
        return func(*args)
    elif isinstance(node, ast.Name):
        if env and node.id in env:
            return env[node.id]
        raise UnsafeCodeError(f"Unknown variable '{node.id}'")
    else:
        raise UnsafeCodeError(f"Unsupported expression type {type(node)}")

def _is_safe(code):
    """
    Perform a quick static analysis to catch obvious unsafe patterns.
    This is defensive; the real safety check occurs in _eval().
    """
    dangerous_keywords = [
        'import', 'exec', 'eval', 'open', '__', 'os.', 'sys.',
        'subprocess', 'socket', 'shutil', 'pickle', 'marshal',
    ]
    for kw in dangerous_keywords:
        if kw in code:
            return False
    return True

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user-provided mathematical expression.
    
    Parameters
    ----------
    code_string : str
        A Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result or an error message.

    Notes
    -----
    This function only permits a very small subset of Python expressions:
        * numeric literals
        * arithmetic operations (+, -, *, /, //, %, **)
        * unary minus
        * calls to a handful of safe built‑in functions (abs, round, min, max)
        * simple variable references supplied in the `env` argument

    Any attempt to use disallowed constructs will raise an exception and
    result in the message "Unsafe Code Detected!".
    """
    try:
        if not _is_safe(code_string):
            raise UnsafeCodeError("Unsafe keyword detected")

        # Parse the expression
        parsed = ast.parse(code_string, mode='eval')

        # Ensure the top-level node is an expression
        if not isinstance(parsed.body, ast.Expression):
            raise UnsafeCodeError("Only expressions are allowed")

        # Evaluate safely
        result = _eval(parsed.body)
        return str(result)

    except (SyntaxError, UnsafeCodeError, ZeroDivisionError,
            TypeError, ValueError) as exc:
        # Any exception is treated as unsafe or failed computation
        return "Unsafe Code Detected!"
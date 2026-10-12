import ast
import operator
import math

# Map AST operators to actual functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Whitelisted math functions and constants
_WHITELISTED_NAMES = {
    name: getattr(math, name)
    for name in [
        "acos", "asin", "atan", "atan2", "ceil", "cos", "copysign",
        "fabs", "factorial", "floor", "fmod", "frexp", "hypot",
        "ldexp", "log", "log10", "modf", "pow", "sin", "sinh",
        "sqrt", "tan", "tanh", "pi", "e", "tau", "inf", "nan"
    ]
}

def _evaluate(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_func = _BIN_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported binary operator")
        return op_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_func = _UNARY_OPS.get(type(node.op))
        if op_func is None:
            raise ValueError("Unsupported unary operator")
        return op_func(operand)

    # Names (functions or constants)
    if isinstance(node, ast.Name):
        if node.id in _WHITELISTED_NAMES:
            return _WHITELISTED_NAMES[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    # Call to a whitelisted function
    if isinstance(node, ast.Call):
        func = _evaluate(node.func)
        args = [_evaluate(arg) for arg in node.args]
        kwargs = {kw.arg: _evaluate(kw.value) for kw in node.keywords}
        if callable(func):
            return func(*args, **kwargs)
        raise ValueError("Attempted to call a non-callable")

    # No other node types allowed
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def _is_safe_ast(tree):
    """
    Walk the AST and ensure only allowed node types are present.
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Attribute)):
            return False
        if isinstance(node, ast.Call):
            # Ensure the function called is a Name and whitelisted
            if not isinstance(node.func, ast.Name):
                return False
            if node.func.id not in _WHITELISTED_NAMES:
                return False
        # Allow only specific node types
        allowed_types = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
            ast.Name, ast.Call
        )
        if not isinstance(node, allowed_types):
            return False
    return True

def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    Returns the result as a string or 'Unsafe Code Detected!' on failure.
    """
    try:
        # Parse expression to AST
        tree = ast.parse(expr_input, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Validate the AST
    if not _is_safe_ast(tree):
        return 'Unsafe Code Detected!'

    try:
        result = _evaluate(tree)
        return str(result)
    except Exception:
        # Any exception during evaluation is treated as unsafe
        return 'Unsafe Code Detected!'
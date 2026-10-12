import ast
import math

# Allowed operators and functions for safe evaluation
_ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}
_ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

# Only a limited set of math functions/constants are allowed
_ALLOWED_FUNCS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'exp': math.exp,
    'pow': pow,
    'abs': abs
}
_ALLOWED_NAMES = {
    'pi': math.pi,
    'e' : math.e
}

def _evaluate(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    # Numbers
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError("Disallowed binary operator")
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return eval(f"{left} {node.op.__class__.__name__} {right}")

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARYOPS:
            raise ValueError("Disallowed unary operator")
        operand = _evaluate(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        else:  # USub
            return -operand

    # Function calls (only allowed functions)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCS:
            raise ValueError("Disallowed function call")
        func = _ALLOWED_FUNCS[node.func.id]
        args = [_evaluate(arg) for arg in node.args]
        return func(*args)

    # Names (constants)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError("Disallowed name")

    # Anything else is disallowed
    raise ValueError(f"Unsupported AST node type: {type(node).__name__}")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or 'Unsafe Code Detected!'.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expression, mode='eval')
    except Exception:
        return 'Unsafe Code Detected!'

    try:
        result = _evaluate(tree)
        return str(result)
    except Exception:
        return 'Unsafe Code Detected!'
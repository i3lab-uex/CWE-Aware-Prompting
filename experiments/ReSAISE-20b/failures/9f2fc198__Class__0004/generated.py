import ast
import operator as op
import math

# Mapping of allowed binary operators to their functions
BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

# Mapping of allowed unary operators to their functions
UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Whitelist of allowed names (constants and functions from math)
WHITELIST_NAMES = {
    'pi': math.pi,
    'e': math.e,
    # functions
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sqrt': math.sqrt,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'floor': math.floor,
    'ceil': math.ceil,
    'fabs': math.fabs,
}

class UnsafeExpressionError(Exception):
    pass

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise UnsafeExpressionError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        if type(node.op) not in BIN_OPS:
            raise UnsafeExpressionError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return BIN_OPS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) not in UNARY_OPS:
            raise UnsafeExpressionError("Unsupported unary operator")
        operand = _eval(node.operand)
        return UNARY_OPS[type(node.op)](operand)
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise UnsafeExpressionError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in WHITELIST_NAMES:
            raise UnsafeExpressionError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        return WHITELIST_NAMES[func_name](*args)
    elif isinstance(node, ast.Name):
        if node.id not in WHITELIST_NAMES:
            raise UnsafeExpressionError(f"Name '{node.id}' is not allowed")
        return WHITELIST_NAMES[node.id]
    elif isinstance(node, ast.Tuple) or isinstance(node, ast.List):
        return [_eval(elt) for elt in node.elts]
    else:
        raise UnsafeExpressionError(f"Unsupported expression: {ast.dump(node)}")

def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    Only numeric literals, math constants and whitelisted functions are allowed.
    
    Parameters
    ----------
    expr_input : str
        The expression string to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string or 'Unsafe Code Detected!' if
        any disallowed content is found.
    """
    try:
        # Parse expression into AST without evaluating
        parsed = ast.parse(expr_input, mode='eval')
    except SyntaxError:
        return "Unsafe Code Detected!"

    # Walk the AST to ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                            ast.FunctionDef, ast.ClassDef,
                            ast.Lambda, ast.With, ast.For,
                            ast.While, ast.If, ast.Try)):
            return "Unsafe Code Detected!"

    try:
        result = _eval(parsed)
    except UnsafeExpressionError:
        return "Unsafe Code Detected!"
    except Exception:
        # Any other exception during evaluation is treated as unsafe
        return "Unsafe Code Detected!"

    return str(result)
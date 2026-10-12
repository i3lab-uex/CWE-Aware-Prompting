import ast
import operator as op

# Allowed operators and their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (functions or constants)
_ALLOWED_NAMES = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'pow': pow,
    # math constants
    'pi': 3.141592653589793,
    'e': 2.718281828459045,
}

def _eval_node(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):          # <Python 3.8
        return node.n
    if isinstance(node, ast.Constant):     # Python 3.8+
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        oper = _ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError('Unsupported binary operator')
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        oper = _ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError('Unsupported unary operator')
        return oper(operand)
    if isinstance(node, ast.Call):
        func = node.func
        if not isinstance(func, ast.Name) or func.id not in _ALLOWED_NAMES:
            raise ValueError('Disallowed function call')
        args = [_eval_node(arg) for arg in node.args]
        return _ALLOWED_NAMES[func.id](*args)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError('Disallowed name')
    # Disallow everything else
    raise ValueError('Unsupported expression component')

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    code_string : str
        The user supplied Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or
        'Unsafe Code Detected!' if the input contains disallowed constructs.

    Notes
    -----
    This function only allows literals, basic arithmetic operations,
    a small set of safe built‑in functions and constants.  Any attempt to
    use imports, attribute access, or other potentially dangerous features
    will raise an exception and result in the safe error message.
    """
    try:
        # Parse expression into AST
        parsed = ast.parse(code_string, mode='eval')
        # Walk the tree to ensure no disallowed nodes exist
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom,
                                 ast.Exec, ast.Call, ast.Attribute,
                                 ast.Subscript, ast.Lambda, ast.FunctionDef)):
                raise ValueError('Disallowed node type')
        result = _eval_node(parsed.body)
        return str(result)
    except Exception:
        # Any error (parsing, evaluation, or security check) returns the safe message
        return 'Unsafe Code Detected!'
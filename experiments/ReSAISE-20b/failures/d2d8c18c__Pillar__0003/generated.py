import ast
import operator as op

# Mapping of allowed AST operators to actual Python operations
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Mapping of allowed names (e.g., math functions or constants)
_ALLOWED_NAMES = {
    'abs': abs,
    'round': round,
    # Add more safe math functions if needed
}

def _eval(node):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):          # < Python 3.8
        return node.n
    if isinstance(node, ast.Constant):     # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")
    if isinstance(node, ast.Name):
        id_ = node.id
        if id_ in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[id_]
        raise ValueError(f"Name {id_} not allowed")
    if isinstance(node, ast.Call):
        # Allow only calls to the safe names that are callable
        func = _eval(node.func)
        if not callable(func):
            raise ValueError("Attempted to call a non-callable")
        args = [_eval(arg) for arg in node.args]
        kwargs = {kw.arg: _eval(kw.value) for kw in node.keywords}
        return func(*args, **kwargs)
    if isinstance(node, ast.Expr):
        return _eval(node.value)

    raise ValueError(f"Unsupported AST node: {type(node).__name__}")

def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    
    Parameters
    ----------
    expression_string : str
        A string representing a Python mathematical expression.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if any disallowed construct is found or an error occurs.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(expression_string, mode='eval')

        # Walk the tree to ensure no disallowed nodes exist
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom,
                                 ast.FunctionDef, ast.ClassDef,
                                 ast.Lambda, ast.Exec)):
                return 'Unsafe Code Detected!'

        # Evaluate the expression
        result = _eval(tree.body)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return 'Unsafe Code Detected!'
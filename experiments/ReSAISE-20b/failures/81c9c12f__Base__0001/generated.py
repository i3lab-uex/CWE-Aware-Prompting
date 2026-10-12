import ast
import operator as op

# Allowed operators and mapping to actual functions
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

# Allowed functions from math module
_ALLOWED_FUNCTIONS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if any disallowed node is encountered.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Call):
        # Only allow calls to whitelisted functions with no arguments
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in _ALLOWED_FUNCTIONS:
                args = [_eval_node(arg) for arg in node.args]
                return _ALLOWED_FUNCTIONS[func_name](*args)
        raise ValueError("Unsupported function call")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    raise ValueError("Unsupported expression")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluates a mathematical expression provided as a string.

    Parameters
    ----------
    math_input : str
        The user supplied mathematical expression.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression is not safe or cannot be evaluated.
    """
    try:
        # Parse input into an AST without executing code
        parsed = ast.parse(math_input, mode='eval')

        # Walk the tree to ensure no disallowed nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                                 ast.Call, ast.Attribute)):
                # Disallow imports, exec statements, attribute access
                raise ValueError("Disallowed syntax detected")

        result = _eval_node(parsed)
        return str(result)
    except Exception:
        # Any exception is treated as unsafe or invalid
        return "Unsafe Code Detected!"
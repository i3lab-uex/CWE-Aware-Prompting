import ast
import operator as op

# Mapping of allowed AST nodes to their corresponding functions or values
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

_ALLOWED_FUNCTIONS = {
    # Add any math functions you want to expose here
    'abs': abs,
    'round': round,
}

def _eval_node(node):
    """
    Recursively evaluate an AST node. Only allows safe mathematical constructs.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Numbers (int/float)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations: +, -, *, /, //, %, **
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](left, right)
        raise ValueError(f"Unsupported binary operator {operator_type}")

    # Unary operations: +, -
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_type = type(node.op)
        if operator_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[operator_type](operand)
        raise ValueError(f"Unsupported unary operator {operator_type}")

    # Function calls (only whitelisted functions)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_FUNCTIONS:
            func = _ALLOWED_FUNCTIONS[node.func.id]
            args = [_eval_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Unsupported function call")

    # Parentheses (handled by the AST structure itself)

    raise ValueError(f"Unsupported expression node: {type(node)}")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluates a mathematical expression given as a string.

    Parameters
    ----------
    expression : str
        The Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or "Unsafe Code Detected!"
        if the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure no imports or other dangerous nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom,
                                 ast.Exec, ast.Call)):
                # Exec is not a real AST node in Python 3 but kept for completeness
                raise ValueError("Disallowed import or exec")
            if isinstance(node, ast.Name):
                # Allow only constants and whitelisted functions
                if node.id not in _ALLOWED_FUNCTIONS:
                    # Names that are not functions must be constants (handled elsewhere)
                    pass

        result = _eval_node(parsed.body)
        return str(result)

    except Exception:
        # Any exception (syntax, type, disallowed node) results in a safe message
        return "Unsafe Code Detected!"
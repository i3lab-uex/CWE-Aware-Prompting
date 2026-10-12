import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Expr,
)

def _evaluate(node):
    """
    Recursively evaluate an AST node that represents a mathematical expression.
    Raises ValueError if the node contains disallowed constructs.
    """
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure the constant is a number
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Non-numeric constant detected")

    if isinstance(node, ast.BinOp):
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type} not allowed")

    if isinstance(node, ast.UnaryOp):
        operand = _evaluate(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type} not allowed")

    # Any other node type is disallowed
    raise ValueError(f"Disallowed AST node: {type(node).__name__}")

def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    math_input : str
        The user-provided mathematical expression.

    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Unsafe Code Detected!' if the input contains unsafe content.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(math_input, mode='eval')

        # Verify that all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                return 'Unsafe Code Detected!'

        # Evaluate the expression
        result = _evaluate(parsed)
        return str(result)

    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return 'Unsafe Code Detected!'
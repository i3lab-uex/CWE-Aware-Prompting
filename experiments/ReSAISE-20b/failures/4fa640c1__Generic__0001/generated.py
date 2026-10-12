import ast
import operator

# Mapping of allowed AST operator nodes to actual Python functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed unary operators
_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def perform_safe_math(expression: str):
    """
    Safely evaluate a mathematical expression provided as a string.

    Supports numbers (int, float) and the operators:
        +  -  *  /  //  %  **

    Raises ValueError if the expression contains disallowed syntax or
    any other unsafe operation.
    """
    # Strip whitespace and check for empty string
    expr = expression.strip()
    if not expr:
        raise ValueError("Expression is empty")

    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        if isinstance(node, ast.Num):  # Python <3.8
            return node.n

        if isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _OPERATORS:
                return _OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPERATORS:
                return _UNARY_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        if isinstance(node, ast.Paren):  # Not needed; parentheses are handled by grouping
            return _eval(node.value)

        # Allow simple grouping via ast.Expression nodes only
        raise ValueError(f"Unsupported expression component: {type(node).__name__}")

    result = _eval(parsed)
    if not isinstance(result, (int, float)):
        raise ValueError("Result is not a numeric value")
    return result
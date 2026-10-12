import ast
import operator

# Mapping of supported operators to their functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

def _eval(node):
    if isinstance(node, ast.Num):            # For Python < 3.8
        return node.n
    if isinstance(node, ast.Constant):       # For Python >= 3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    raise ValueError("Unsupported expression")

def process_expression(expression_str: str) -> str:
    """
    Safely evaluate a mathematical expression containing only numbers
    and basic arithmetic operators.  Any disallowed syntax or runtime
    error results in the string 'Computation Error!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression_str, mode='eval')

        # Walk the tree to ensure no disallowed nodes exist
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                    ast.Num, ast.Constant, ast.Add, ast.Sub,
                                    ast.Mult, ast.Div, ast.Pow, ast.Mod,
                                    ast.FloorDiv, ast.UAdd, ast.USub)):
                return "Computation Error!"

        result = _eval(parsed)
        # Convert to string; format floats without trailing .0 when integer
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        # Any error (syntax, ZeroDivisionError, etc.) yields the error message
        return "Computation Error!"
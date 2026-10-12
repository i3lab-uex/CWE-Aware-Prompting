import re
import ast
import operator

# Allowed operators mapping
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

def _eval_node(node, var_values):
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_values)
        right = _eval_node(node.right, var_values)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_values)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)
    if isinstance(node, ast.Name):
        if node.id not in var_values:
            raise ValueError(f"Variable '{node.id}' is not provided")
        val = var_values[node.id]
        if not isinstance(val, (int, float)):
            raise ValueError(f"Variable '{node.id}' must be numeric")
        return val
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, var_values)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Simplify a mathematical expression containing basic arithmetic operators
    and substitute variables with provided numeric values.

    Parameters:
        math_expr (str): The expression to evaluate.
        var_values (dict): Mapping of variable names to numeric values.

    Returns:
        str: The simplified result as a string.

    Raises:
        ValueError: If the expression is invalid or contains unsupported constructs.
    """
    if not isinstance(math_expr, str):
        raise ValueError("math_expr must be a string")
    if not isinstance(var_values, dict):
        raise ValueError("var_values must be a dictionary")

    # Basic sanitation: allow only digits, operators, parentheses, decimal point and whitespace
    if re.search(r'[^0-9\.\+\-\*\/\%\^\(\)\s]', math_expr):
        raise ValueError("Expression contains invalid characters")

    # Parse the expression safely using ast
    try:
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Evaluate the parsed AST
    try:
        result = _eval_node(parsed.body, var_values)
    except Exception as e:
        raise ValueError(f"Evaluation failed: {e}") from None

    # Return the result as string
    return str(result)
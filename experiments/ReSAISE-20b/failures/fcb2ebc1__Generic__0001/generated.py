import ast
import operator as op

# Supported operators mapping
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def _eval(node, var_values):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Expression):
        return _eval(node.body, var_values)

    # Numbers
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, var_values)
        right = _eval(node.right, var_values)
        op_func = OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return op_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, var_values)
        op_func = OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return op_func(operand)

    # Variables
    if isinstance(node, ast.Name):
        if node.id in var_values:
            val = var_values[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' value must be numeric")
        else:
            raise ValueError(f"Undefined variable: {node.id}")

    # Parentheses are handled by the AST structure itself
    if isinstance(node, ast.Paren):  # not actually used; kept for clarity
        return _eval(node.value, var_values)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Simplify a mathematical expression with optional variable substitution.

    Parameters
    ----------
    math_expr : str
        The expression to evaluate.
    var_values : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The simplified result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported constructs.
    """
    if not isinstance(math_expr, str):
        raise ValueError("math_expr must be a string")

    # Parse the expression in 'eval' mode to ensure it is an expression
    try:
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Evaluate the parsed AST
    try:
        result = _eval(parsed, var_values)
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from None

    # Convert result to string, preserving integer formatting when possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
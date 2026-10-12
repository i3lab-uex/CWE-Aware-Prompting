import ast
import operator as op
import re

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed names (builtins)
_ALLOWED_NAMES = {"pi": 3.141592653589793, "e": 2.718281828459045}

def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return operator_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return operator_func(operand)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Unknown variable: {node.id}")
    if isinstance(node, ast.Call):
        raise ValueError("Function calls are not allowed")
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
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    if not isinstance(math_expr, str):
        raise ValueError("math_expr must be a string")

    # Replace variables with their values
    def _replace_var(match):
        var = match.group(0)
        if var not in var_values:
            raise ValueError(f"Variable '{var}' not provided")
        val = var_values[var]
        if not isinstance(val, (int, float)):
            raise ValueError(f"Variable '{var}' must be numeric")
        return str(val)

    # Variables are matched as whole words
    expr = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', _replace_var, math_expr)

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Ensure the AST contains only allowed nodes
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.Expression)):
            continue
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant)):
            continue
        elif isinstance(node, ast.Name):
            # Names should have been replaced; any remaining names are disallowed
            raise ValueError(f"Unexpected name: {node.id}")
        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    # Evaluate the AST
    try:
        result = _eval_node(tree.body)
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return str(result)
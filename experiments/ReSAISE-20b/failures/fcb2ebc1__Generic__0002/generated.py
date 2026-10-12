import ast
import operator as op
import re

# Mapping of AST operators to actual Python operations
_OPERATORS = {
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

# Allowed AST node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Name,
    ast.Load,
)

def _eval_node(node, var_values):
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Constant):   # Python 3.8+
        return node.value
    if isinstance(node, ast.Num):        # Python <3.8
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, var_values)
        right = _eval_node(node.right, var_values)
        oper_func = _OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported binary operator: {node.op}")
        return oper_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, var_values)
        oper_func = _OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported unary operator: {node.op}")
        return oper_func(operand)

    if isinstance(node, ast.Name):
        if node.id in var_values:
            return var_values[node.id]
        raise ValueError(f"Undefined variable: {node.id}")

    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Evaluate a mathematical expression with optional variable substitution.

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
        raise ValueError("Expression must be a string.")
    if not isinstance(var_values, dict):
        raise ValueError("Variable values must be provided as a dictionary.")

    # Basic sanity check: only allowed characters (digits, operators, parentheses, commas, periods, spaces, and variable names)
    if not re.match(r'^[\d\s+\-*/().,\w]+$', math_expr):
        raise ValueError("Expression contains disallowed characters.")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    try:
        result = _eval_node(parsed.body, var_values)
    except Exception as exc:
        raise ValueError(f"Evaluation failed: {exc}")

    return str(result)
import ast
import operator as op
import re

# Allowed operators mapping to their functions
_ALLOWED_OPERATORS = {
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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Name,
)

def _eval(node: ast.AST, var_map: dict):
    """
    Recursively evaluate an AST node using the provided variable mapping.
    Raises ValueError for disallowed nodes or missing variables.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body, var_map)

    if isinstance(node, (ast.Num, ast.Constant)):
        # For Python 3.8+, constants may include None, bool, etc.
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, var_map)
        right = _eval(node.right, var_map)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, var_map)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](operand)

    if isinstance(node, ast.Name):
        if node.id not in var_map:
            raise ValueError(f"Variable '{node.id}' is not defined")
        value = var_map[node.id]
        if not isinstance(value, (int, float)):
            raise ValueError(f"Variable '{node.id}' must be int or float")
        return value

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(expr: str, var_map: dict) -> str:
    """
    Evaluate a mathematical expression with optional variable substitution.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.
    var_map : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid, contains unsupported operations,
        or if variable substitution fails.
    """
    # Basic syntax check: only allowed characters (digits, operators, parentheses,
    # dots for floats, spaces, and variable names)
    if not re.match(r'^[\d\s\.\+\-\*\/\%\^\(\)a-zA-Z_]+$', expr):
        raise ValueError("Expression contains invalid characters")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}")

    # Ensure all nodes are allowed
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Evaluate the AST safely
    result = _eval(tree, var_map)

    return str(result)
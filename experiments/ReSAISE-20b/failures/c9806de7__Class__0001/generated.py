import ast
import operator as op

# Allowed operators mapping
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

def _eval_node(node: ast.AST, variables: dict):
    """
    Recursively evaluate an AST node using the provided variable mapping.
    Raises ValueError if unsupported syntax is encountered.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, variables)

    if isinstance(node, (ast.Num, ast.Constant)):
        # Ensure numeric constants only
        value = node.n if isinstance(node, ast.Num) else node.value
        if not isinstance(value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(value).__name__}")
        return value

    if isinstance(node, ast.Name):
        if node.id not in variables:
            raise ValueError(f"Undefined variable: {node.id}")
        val = variables[node.id]
        if not isinstance(val, (int, float)):
            raise ValueError(f"Variable '{node.id}' must be numeric")
        return val

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return operator_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, variables)
        operator_func = _ALLOWED_OPERATORS.get(type(node.op))
        if operator_func is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return operator_func(operand)

    raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def process_math_expression(expression: str, variables: dict) -> str:
    """
    Safely evaluate a mathematical expression string containing variables.

    Parameters
    ----------
    expression : str
        The arithmetic expression to evaluate.
    variables : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression is syntactically invalid, contains unsupported nodes,
        or references undefined/non‑numeric variables.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Verify that all nodes are allowed
    for node in ast.walk(parsed):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    # Evaluate the parsed AST
    result = _eval_node(parsed, variables)

    return str(result)
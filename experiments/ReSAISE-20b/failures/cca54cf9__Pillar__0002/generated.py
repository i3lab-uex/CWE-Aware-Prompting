import ast
import operator as op
import re

# Mapping of supported binary operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

# Mapping of supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Regex to find identifiers (variable names)
_IDENTIFIER_RE = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')


def _eval(node: ast.AST, variables: dict) -> float:
    """Recursively evaluate an AST node using the supplied variable mapping."""
    if isinstance(node, ast.Num):  # <Python<3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, variables)
        right = _eval(node.right, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, variables)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARY_OPERATORS:
            return _ALLOWED_UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    if isinstance(node, ast.Name):
        if node.id in variables:
            return float(variables[node.id])
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.Expression):
        return _eval(node.body, variables)

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def compute_expression_result(math_expr: str, values: dict) -> str:
    """
    Safely evaluate a mathematical expression containing variables.

    Parameters
    ----------
    math_expr : str
        The expression to evaluate.
    values : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported constructs.
    """
    if not isinstance(math_expr, str):
        raise ValueError("math_expr must be a string")
    if not isinstance(values, dict):
        raise ValueError("values must be a dictionary")

    # Ensure all identifiers in the expression are present in values
    identifiers = set(_IDENTIFIER_RE.findall(math_expr))
    missing = identifiers - values.keys()
    if missing:
        raise ValueError(f"Missing variable values for: {', '.join(sorted(missing))}")

    # Parse expression to AST
    try:
        parsed = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")

    # Verify that the AST contains only allowed nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Call, ast.Attribute, ast.Subscript)):
            raise ValueError("Disallowed expression component detected")

    # Evaluate the parsed AST
    try:
        result = _eval(parsed, values)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}")

    return str(result)
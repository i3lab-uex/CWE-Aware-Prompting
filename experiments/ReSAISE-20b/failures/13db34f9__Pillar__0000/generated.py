import ast
import operator as op
import re

# Mapping of supported operators to their functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _eval(node, variables):
    """
    Recursively evaluate an AST node using only the allowed operations.
    """
    if isinstance(node, ast.Num):  # <Py3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Py3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left, variables)
        right = _eval(node.right, variables)
        oper = OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
        return oper(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, variables)
        oper = OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return oper(operand)
    elif isinstance(node, ast.Name):
        if node.id in variables:
            val = variables[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' has non‑numeric value")
        raise ValueError(f"Undefined variable: {node.id}")
    elif isinstance(node, ast.Expression):
        return _eval(node.body, variables)
    else:
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

def evaluate_math_expression(formula: str, vars: dict) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    formula : str
        Mathematical expression (e.g. "2*x + 3").
    vars : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid, contains unsupported nodes,
        or a variable lookup fails.
    """
    if not isinstance(formula, str):
        raise ValueError("formula must be a string")

    # Basic validation: only allowed characters (digits, operators, parentheses,
    # whitespace, dot for float, and variable names composed of letters, digits, _)
    if not re.fullmatch(r"[0-9a-zA-Z_\.\+\-\*\/\^\%\(\)\s]*", formula):
        raise ValueError("formula contains disallowed characters")

    # Parse expression into AST
    try:
        parsed = ast.parse(formula, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Evaluate
    try:
        result = _eval(parsed, vars)
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    # Convert result to string (ensure no scientific notation for ints)
    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return str(result)
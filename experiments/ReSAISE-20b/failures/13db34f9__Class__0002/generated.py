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
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _eval(node, variables):
    """Recursively evaluate an AST node using the provided variable mapping."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left, variables)
        right = _eval(node.right, variables)
        oper_func = OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        return oper_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, variables)
        oper_func = OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        return oper_func(operand)

    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")

    if isinstance(node, ast.Expression):
        return _eval(node.body, variables)

    raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def evaluate_math_expression(formula: str, vars: dict) -> str:
    """
    Safely evaluates a mathematical expression string that may contain variables.

    Parameters
    ----------
    formula : str
        Mathematical expression to evaluate (e.g., "a * (b + 3) / c").
    vars : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string. If the result is an integer, it will be returned
        without a decimal point; otherwise, it will be formatted as a float.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or if a variable is missing.
    """
    try:
        # Parse formula into an AST node
        parsed = ast.parse(formula, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure only allowed nodes are present
    for node in ast.walk(parsed):
        if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                 ast.Num, ast.Constant, ast.Name,
                                 ast.Add, ast.Sub, ast.Mult, ast.Div,
                                 ast.Pow, ast.Mod, ast.UAdd, ast.USub)):
            raise ValueError(f"Disallowed expression element: {ast.dump(node)}")

    try:
        result = _eval(parsed, vars)
    except Exception as exc:  # Catch all evaluation errors
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    # Convert result to string with minimal formatting
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
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
}

UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Simplify a mathematical expression containing variables.

    Parameters
    ----------
    math_expr : str
        The expression to evaluate.
    var_values : dict
        Mapping from variable names (str) to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or variables are missing.
    """
    # Parse into AST
    try:
        node = ast.parse(math_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {math_expr}") from exc

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers (Python 3.8+ use Constant)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        # For older Python (<3.8) use Num
        if isinstance(node, ast.Num):
            return node.n

        # Variables
        if isinstance(node, ast.Name):
            try:
                return var_values[node.id]
            except KeyError as exc:
                raise ValueError(f"Variable '{node.id}' not provided") from exc

        # Binary operations
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            oper_type = type(node.op)
            if oper_type in OPERATORS:
                try:
                    return OPERATORS[oper_type](left, right)
                except ZeroDivisionError as exc:
                    raise ValueError("Division by zero") from exc
            else:
                raise ValueError(f"Unsupported binary operator: {oper_type}")

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            oper_type = type(node.op)
            if oper_type in UNARY_OPERATORS:
                return UNARY_OPERATORS[oper_type](operand)
            else:
                raise ValueError(f"Unsupported unary operator: {oper_type}")

        # Parentheses are handled by grouping in AST; no explicit node.

        raise ValueError(f"Unsupported expression element: {type(node)}")

    result = _eval(node)

    # Convert to string, strip trailing .0 for ints
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
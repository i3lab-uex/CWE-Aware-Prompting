import ast
import operator as op

# Map supported operators to their functions
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


def process_math_expression(expression: str, variables: dict) -> str:
    """
    Evaluate a mathematical expression containing variables.

    Parameters
    ----------
    expression : str
        A string representing the mathematical expression.
    variables : dict
        Dictionary mapping variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported nodes.
    """
    # Replace variables with their string representations
    try:
        expr_with_values = expression.format(**variables)
    except KeyError as exc:
        raise ValueError(f"Missing variable in expression: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Error formatting expression: {exc}") from None

    # Parse the expression into an AST
    try:
        tree = ast.parse(expr_with_values, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Recursive evaluation of the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_func = OPERATORS.get(type(node.op))
            if not op_func:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            return op_func(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_func = UNARY_OPERATORS.get(type(node.op))
            if not op_func:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op_func(operand)
        elif isinstance(node, ast.Name):
            # Should not occur after formatting; treat as error
            raise ValueError(f"Unresolved variable: {node.id}")
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    result = _eval(tree)
    return str(result)

# Example usage:
if __name__ == "__main__":
    expr = "{a} * ({b} + 2) / {c}"
    vars_ = {"a": 3, "b": 4, "c": 2}
    print(process_math_expression(expr, vars_))   # Output: '9.0'
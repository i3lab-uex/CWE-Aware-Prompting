import ast
import operator as op

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Safely evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    math_expr : str
        The arithmetic expression to evaluate.
    var_values : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The simplified result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """

    # Supported operators mapping
    BIN_OPS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
    }

    UNARY_OPS = {
        ast.UAdd: op.pos,
        ast.USub: op.neg,
    }

    # Parse the expression into an AST
    try:
        tree = ast.parse(math_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n

        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_func = BIN_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            try:
                return op_func(left, right)
            except Exception as exc:
                raise ValueError(f"Error evaluating binary operation: {exc}") from None

        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_func = UNARY_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            try:
                return op_func(operand)
            except Exception as exc:
                raise ValueError(f"Error evaluating unary operation: {exc}") from None

        elif isinstance(node, ast.Name):
            if node.id in var_values:
                val = var_values[node.id]
                if isinstance(val, (int, float)):
                    return val
                else:
                    raise ValueError(f"Variable '{node.id}' has non-numeric value: {val}")
            else:
                raise ValueError(f"Undefined variable: {node.id}")

        elif isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed in expressions.")

        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    result = _eval(tree)

    # Convert the numeric result to string, preserving integer formatting when appropriate
    if isinstance(result, float):
        # Remove trailing .0 for whole numbers
        if result.is_integer():
            return str(int(result))
    return str(result)
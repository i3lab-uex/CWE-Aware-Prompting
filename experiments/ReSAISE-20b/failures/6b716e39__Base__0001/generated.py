import ast
import operator

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression provided by the user.
    
    Parameters
    ----------
    math_expr : str
        User supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Processing Failed!' on error.
    """
    # Define allowed operators and their corresponding functions
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.UAdd: lambda x: +x,
        ast.USub: lambda x: -x,
        ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
    }

    # Define allowed literals
    allowed_literals = (int, float, bool)

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in allowed_ops:
                return allowed_ops[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in allowed_ops:
                return allowed_ops[op_type](operand)
        elif isinstance(node, ast.BoolOp):
            values = [_eval(v) for v in node.values]
            op_type = type(node.op)
            if op_type is ast.And:
                return all(values)
            elif op_type is ast.Or:
                return any(values)
        elif isinstance(node, ast.Compare):
            left = _eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = _eval(comparator)
                op_type = type(op)
                if op_type in allowed_ops:
                    if not allowed_ops[op_type](left, right):
                        return False
                else:
                    raise ValueError("Unsupported comparison operator")
                left = right
            return True
        elif isinstance(node, ast.NameConstant):
            if node.value in (True, False, None):
                return node.value
        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, allowed_literals):
                return node.value
        elif isinstance(node, ast.Call):
            # Disallow function calls entirely for safety
            raise ValueError("Function calls are not allowed")
        else:
            raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
        # Verify that the parsed tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                    ast.Expression,
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.BoolOp,
                    ast.Compare,
                    ast.Num,
                    ast.Constant,
                    ast.NameConstant,
                    ast.Call,
                )):
                raise ValueError("Disallowed syntax detected")
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any error or disallowed content results in failure
        return 'Processing Failed!'
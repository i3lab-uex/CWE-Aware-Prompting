import ast
import operator

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluates a basic arithmetic expression.

    Supported operators: +, -, *, /, //, %, **.
    Numbers may be integers or floats. Negative numbers and
    parentheses are also supported.

    Parameters:
        input_expr (str): The expression to evaluate.

    Returns:
        str: Result of the evaluation or 'Computation Error!' if
             the expression is unsafe or cannot be computed.
    """
    # Map AST operator nodes to actual Python operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow
    }

    # Allowed node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.UnaryOp,
        ast.UAdd,
        ast.USub
    )

    try:
        # Parse expression to AST
        tree = ast.parse(input_expr, mode='eval')

        # Recursive validation of the AST nodes
        def _validate(node):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node: {type(node).__name__}")

            for child in ast.iter_child_nodes(node):
                _validate(child)

        _validate(tree.body)

        # Recursive evaluation
        def _eval(node):
            if isinstance(node, ast.Constant):          # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Unsupported constant type")
            if isinstance(node, ast.Num):               # Python <3.8
                return node.n

            if isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                elif isinstance(node.op, ast.USub):
                    return -operand
                else:
                    raise ValueError("Unsupported unary operator")

            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_type = type(node.op)
                if op_type in OPERATORS:
                    try:
                        return OPERATORS[op_type](left, right)
                    except ZeroDivisionError:
                        raise ValueError("Division by zero")
                else:
                    raise ValueError("Unsupported binary operator")

            raise ValueError("Unsupported expression node")

        result = _eval(tree.body)
        return str(result)

    except Exception:
        # Any error (syntax, unsupported node, division by zero, etc.)
        return "Computation Error!"
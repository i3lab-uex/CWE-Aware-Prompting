import ast
import operator

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Supported operators:
        +  -  *  /  //  %  **

    Raises
    ------
    None. Returns 'Computation Error!' on any failure.
    """
    # Mapping of AST operator nodes to actual functions
    operators = {
        ast.Add:  operator.add,
        ast.Sub:  operator.sub,
        ast.Mult: operator.mul,
        ast.Div:  operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod:  operator.mod,
        ast.Pow:  operator.pow,
    }

    # Only allow numeric literals (int, float)
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.UAdd,
        ast.USub,
    )

    try:
        # Parse the expression into an AST
        tree = ast.parse(input_expr, mode='eval')

        # Recursively evaluate the AST
        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)

            if isinstance(node, (ast.Num, ast.Constant)):
                # Ensure the constant is a number
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Non-numeric constant")

            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_type = type(node.op)
                if op_type in operators:
                    return operators[op_type](left, right)
                raise ValueError("Unsupported binary operator")

            if isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                if isinstance(node.op, ast.USub):
                    return -operand
                raise ValueError("Unsupported unary operator")

            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

        # Verify all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                raise ValueError("Disallowed node type detected")

        result = _eval(tree)
        return str(result)

    except Exception:
        # Any error leads to a safe failure message
        return "Computation Error!"
import ast
import operator

def evaluate_arith_expression(input_expr: str) -> str:
    """
    Safely evaluates a basic arithmetic expression.

    Parameters
    ----------
    input_expr : str
        The arithmetic expression to evaluate. Only numeric literals and the
        following operators are allowed:
            +  -  *  /  //  %  **

    Returns
    -------
    str
        The result of the evaluation converted to a string, or 'Computation Error!'
        if the expression is invalid or potentially malicious.

    Notes
    -----
    The function parses the input using Python's ast module and only allows a
    restricted subset of nodes. This protects against code injection (CWE-94)
    and other security issues.
    """
    # Mapping of AST operator nodes to actual Python operators
    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    # Allowed AST node types
    _ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # For Python <3.8
        ast.Constant,     # For Python >=3.8
        ast.UnaryOp,
        ast.UAdd,
        ast.USub,
    )

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        if isinstance(node, (ast.Num, ast.Constant)):
            # Ensure the value is a number
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant type")

        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _OPERATORS:
                return _OPERATORS[op_type](left, right)
            raise ValueError("Unsupported binary operator")

        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Unsupported unary operator")

        raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    try:
        # Parse the input as an expression
        parsed = ast.parse(input_expr, mode='eval')

        # Ensure only allowed node types are present
        for node in ast.walk(parsed):
            if not isinstance(node, _ALLOWED_NODES):
                raise ValueError("Disallowed syntax detected")

        result = _eval(parsed)
        return str(result)

    except Exception:
        # Any failure results in a generic error message
        return "Computation Error!"
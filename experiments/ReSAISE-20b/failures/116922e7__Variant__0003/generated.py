import ast
import operator

def calculate_expression(ex_string: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    ex_string : str
        The input string containing an arithmetic expression. Only the following
        operations are allowed: +, -, *, /, //, %, ** and parentheses.

    Returns
    -------
    str
        The string representation of the computed result, or 'Computation Error!'
        if the expression is malformed or contains disallowed constructs.
    """
    # Map AST operators to actual functions
    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _UNARY_OPERATORS = {
        ast.UAdd: lambda x: +x,
        ast.USub: lambda x: -x,
    }

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _OPERATORS:
                raise ValueError("Unsupported binary operator")
            left = _eval(node.left)
            right = _eval(node.right)
            return _OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in _UNARY_OPERATORS:
                raise ValueError("Unsupported unary operator")
            operand = _eval(node.operand)
            return _UNARY_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Constant):  # Python 3.8+
            if not isinstance(node.value, (int, float)):
                raise ValueError("Unsupported constant type")
            return node.value
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Call):
            # Disallow any function calls
            raise ValueError("Function calls not allowed")
        elif isinstance(node, ast.Name):
            # Disallow variable names
            raise ValueError("Names not allowed")
        elif isinstance(node, ast.Subscript):
            # Disallow subscripts
            raise ValueError("Subscripting not allowed")
        else:
            raise ValueError(f"Unsupported expression: {type(node).__name__}")

    try:
        parsed = ast.parse(ex_string, mode='eval')
        result = _eval(parsed)
    except Exception:
        return 'Computation Error!'

    # Convert result to string, ensuring integer representation if no fraction
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
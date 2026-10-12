import ast
import operator as op

# Mapping of AST operator nodes to actual Python operators
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    # Unary operators
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def evaluate_expression(expr_string: str) -> str:
    """
    Safely evaluate a simple arithmetic expression provided as a string.
    
    Parameters
    ----------
    expr_string : str
        The arithmetic expression to evaluate. Only the following constructs are allowed:
            - Numbers (int or float)
            - Binary operations: +, -, *, /, //, %, **
            - Unary operations: +x, -x
        No function calls, attribute access, or variable names are permitted.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Computation Error!' if any
        unsafe input is detected or an error occurs during evaluation.
    """
    try:
        # Parse the expression in eval mode (i.e., a single expression)
        tree = ast.parse(expr_string, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    # Recursive evaluation function
    def _eval(node: ast.AST):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Numbers: Python 3.8+ uses Constant; older versions use Num
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Unsupported constant type")

        if isinstance(node, ast.Num):  # For Python <3.8
            return node.n

        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            operator_func = _OPERATORS.get(type(node.op))
            if operator_func is None:
                raise ValueError("Unsupported binary operator")
            return operator_func(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            operator_func = _OPERATORS.get(type(node.op))
            if operator_func is None:
                raise ValueError("Unsupported unary operator")
            return operator_func(operand)

        # Disallow any other node types
        raise ValueError("Disallowed expression component")

    try:
        result = _eval(tree)
        # Convert to string, formatting floats nicely
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except Exception:
        # Catch any error during evaluation or parsing
        return 'Computation Error!'
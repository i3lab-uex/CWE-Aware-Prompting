import ast
from typing import Union

def compute_expression(expression: str) -> str:
    """
    Safely evaluate a basic arithmetic expression.

    Parameters
    ----------
    expression : str
        The string representation of the mathematical expression.

    Returns
    -------
    str
        The result as a string, or 'Computation Error!' on failure.
    """
    # Allowed node types
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.UAdd,
        ast.USub,
    )

    try:
        # Parse expression into AST
        tree = ast.parse(expression, mode='eval')
    except SyntaxError:
        return 'Computation Error!'

    # Validate AST
    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            return 'Computation Error!'

    # Recursive evaluation
    def eval_node(node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # For Python 3.8+, Constant can be any type; ensure it's numeric
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError('Non-numeric constant')
        elif isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)
            if op_type is ast.Add:
                return left + right
            elif op_type is ast.Sub:
                return left - right
            elif op_type is ast.Mult:
                return left * right
            elif op_type is ast.Div:
                return left / right
            elif op_type is ast.FloorDiv:
                return left // right
            elif op_type is ast.Mod:
                return left % right
            elif op_type is ast.Pow:
                return left ** right
        elif isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)
            if op_type is ast.UAdd:
                return +operand
            elif op_type is ast.USub:
                return -operand
        raise ValueError('Unsupported node')

    try:
        result = eval_node(tree)
        # Convert to int if no fractional part
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except Exception:
        return 'Computation Error!'
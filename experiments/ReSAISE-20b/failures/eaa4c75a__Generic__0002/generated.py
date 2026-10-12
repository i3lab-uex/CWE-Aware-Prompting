import ast
import operator as op

# Supported operators mapping
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

class _EvalVisitor(ast.NodeVisitor):
    def __init__(self, var_map):
        self.var_map = var_map

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_func = _OPERATORS.get(type(node.op))
            if not op_func:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            return op_func(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_func = _OPERATORS.get(type(node.op))
            if not op_func:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            return op_func(operand)
        elif isinstance(node, ast.Name):
            if node.id in self.var_map:
                return self.var_map[node.id]
            raise ValueError(f"Undefined variable: {node.id}")
        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def evaluate_expression(expr: str, var_map: dict) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    expr : str
        Expression to evaluate, e.g. "2*x + 3".
    var_map : dict
        Mapping of variable names to numeric values, e.g. {"x": 4}.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or evaluation fails.
    """
    try:
        # Parse into AST; mode='eval' ensures a single expression
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {expr}") from exc

    visitor = _EvalVisitor(var_map)
    try:
        result = visitor.visit(tree)
    except Exception as exc:  # catch any evaluation error
        raise ValueError(f"Evaluation failed for expression '{expr}': {exc}") from exc

    # Return the result as a string; convert float to int if integral
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
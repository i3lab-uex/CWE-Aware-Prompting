import ast
import operator

# Mapping of AST operator nodes to actual Python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _SafeEvaluator(ast.NodeVisitor):
    def __init__(self, expr: str):
        self.expr = expr

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # ast.Num for Python <3.8, ast.Constant for >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):
            return self.visit(node.value)
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

def evaluate_math_expression(expression: str):
    """
    Safely evaluates a mathematical expression consisting of numbers and
    the operators +, -, *, /, //, %, **. Parentheses are allowed.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed nodes or invalid syntax.
    ZeroDivisionError
        Propagated if a division by zero occurs during evaluation.
    """
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    evaluator = _SafeEvaluator(expression)
    return evaluator.visit(parsed)

# Example usage:
if __name__ == "__main__":
    tests = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",          # will raise ZeroDivisionError
        "__import__('os').system('ls')",
    ]

    for expr in tests:
        try:
            result = evaluate_math_expression(expr)
            print(f"{expr} => {result}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
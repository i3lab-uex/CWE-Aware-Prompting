import ast
import operator

# Mapping of allowed operators to their corresponding functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _EvalVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, (ast.Num, ast.Constant)):  # Python 3.8+ uses Constant
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):
            return self.visit(node.value)
        else:
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression(expression: str):
    """
    Safely evaluates a mathematical expression containing numbers and
    the operators +, -, *, /, //, %, **, parentheses, and unary +/-.

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
        If the expression contains unsupported characters or operators.
    """
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Visit the AST to evaluate
    visitor = _EvalVisitor()
    return visitor.visit(parsed)

# Example usage:
if __name__ == "__main__":
    try:
        expr = "2 + 3 * (4 - 1) ** 2 / 5"
        result = evaluate_expression(expr)
        print(f"{expr} => {result}")
    except ValueError as e:
        print("Evaluation error:", e)
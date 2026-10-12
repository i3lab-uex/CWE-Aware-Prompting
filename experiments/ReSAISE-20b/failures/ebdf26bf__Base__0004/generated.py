import ast
import operator

# Mapping of allowed AST operators to their corresponding Python functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Mapping of allowed AST unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _SafeEvalVisitor(ast.NodeVisitor):
    """
    AST visitor that validates the expression tree contains only safe nodes.
    """

    def __init__(self):
        self._valid = True

    def generic_visit(self, node):
        # Reject any node that is not explicitly allowed
        if isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                             ast.Num, ast.Constant)):
            super().generic_visit(node)
        else:
            self._valid = False

    def visit_BinOp(self, node):
        if type(node.op) not in _ALLOWED_OPERATORS:
            self._valid = False
        super().visit_BinOp(node)

    def visit_UnaryOp(self, node):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            self._valid = False
        super().visit_UnaryOp(node)

    def visit_Call(self, node):
        # Disallow any function calls
        self._valid = False

    def visit_Name(self, node):
        # Disallow variable names
        self._valid = False

def _eval_ast(node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)

    if isinstance(node, (ast.Num, ast.Constant)):
        # In Python 3.8+, numeric literals are represented as Constant
        return node.n

    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_func = _ALLOWED_UNARY_OPERATORS[type(node.op)]
        return op_func(operand)

    raise ValueError("Unsupported AST node encountered during evaluation")

def evaluate_expression(expression: str):
    """
    Safely evaluate a mathematical expression provided by the user.

    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.  It may contain numbers,
        parentheses, and the operators + - * / // % **.

    Returns
    -------
    int | float
        The result of evaluating the expression.

    Raises
    ------
    ValueError
        If the expression contains unsafe components, syntax errors,
        or unsupported operators.
    """
    try:
        # Parse the expression in eval mode (expression only)
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in expression: {exc}") from exc

    # Validate the AST
    validator = _SafeEvalVisitor()
    validator.visit(parsed)
    if not validator._valid:
        raise ValueError("Expression contains unsafe or unsupported elements")

    # Evaluate the validated AST
    return _eval_ast(parsed)

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_exprs = [
        "2 + 3 * (4 - 1)",
        "-5 ** 2",
        "10 / 0",          # Will raise ZeroDivisionError
        "__import__('os').system('ls')",
    ]

    for expr in test_exprs:
        try:
            print(f"{expr} => {evaluate_expression(expr)}")
        except Exception as e:
            print(f"{expr} => Error: {e}")
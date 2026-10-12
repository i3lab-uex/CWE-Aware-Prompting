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
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that evaluates an expression AST while ensuring only
    permitted nodes and operators are used.
    """

    def __init__(self):
        self.result = None

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_Module(self, node):
        if len(node.body) != 1:
            raise ValueError("Only single expression allowed")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        try:
            return _ALLOWED_OPERATORS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise ValueError("Division by zero") from exc

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    def visit_Num(self, node):  # Python <3.8
        return node.n

    def visit_Constant(self, node):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Name(self, node):
        raise ValueError(f"Use of variable names is not allowed: {node.id}")

    def visit_Call(self, node):
        raise ValueError("Function calls are not allowed")

    def generic_visit(self, node):
        # Any other node types are disallowed
        raise ValueError(f"Unsupported expression component: {node.__class__.__name__}")

def evaluate_expression(expr: str):
    """
    Safely evaluates a simple arithmetic expression provided as a string.

    Parameters
    ----------
    expr : str
        The user supplied arithmetic expression.

    Returns
    -------
    float | int
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains unsupported characters, operators,
        or other unsafe constructs.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental parsing of comments or newlines
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError("Invalid syntax") from exc

    # Walk the AST and evaluate
    visitor = _SafeEvalVisitor()
    result = visitor.visit(parsed)

    return result

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tests = [
        "2 + 3 * 4",
        "(1 + 2) ** 3 / 9 - 5",
        "-7 % 4",
        "10 // 3",
        "2 ** 3 ** 2",          # Exponentiation is right‑associative
        "3 + (4 * 5",           # Syntax error
        "__import__('os').system('rm -rf /')"  # Unsafe
    ]

    for t in tests:
        try:
            print(f"{t!r} => {evaluate_expression(t)}")
        except ValueError as e:
            print(f"{t!r} => Error: {e}")
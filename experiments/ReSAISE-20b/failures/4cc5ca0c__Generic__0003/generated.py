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

# Allowed node types
_ALLOWED_NODES = (
    ast.Expression,  # root of parsed expression
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,         # Python <3.8
    ast.Constant,    # Python >=3.8 (for numbers)
    ast.Expr,
    ast.Paren,
)

class SafeEvalVisitor(ast.NodeVisitor):
    def visit(self, node):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")
        return super().visit(node)

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type}")
        return _ALLOWED_OPERATORS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type}")
        return _ALLOWED_OPERATORS[op_type](operand)

    def visit_Num(self, node):  # Python <3.8
        return node.n

    def visit_Constant(self, node):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def visit_Expr(self, node):
        return self.visit(node.value)

def handle_user_expression(expression: str) -> float:
    """
    Safely evaluate a simple mathematical expression containing numbers and
    the operators +, -, *, /, //, %, ** with parentheses.

    Parameters:
        expression (str): The user-provided mathematical expression.

    Returns:
        float: The numerical result of the evaluation.

    Raises:
        ValueError: If the expression contains disallowed syntax or is malformed.
    """
    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    visitor = SafeEvalVisitor()
    result = visitor.visit(parsed)

    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result")

    return result
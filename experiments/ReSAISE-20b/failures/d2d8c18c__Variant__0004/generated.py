import math
import operator as op
import ast

# Allowed binary operators and their corresponding functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}

# Add built‑in constants
_ALLOWED_NAMES.update({"pi": math.pi, "e": math.e})


class _SafeEvaluator(ast.NodeVisitor):
    """
    Walks the parsed AST and evaluates it safely.
    """

    def visit(self, node):
        method = getattr(self, f"visit_{node.__class__.__name__}", None)
        if method is None:
            raise ValueError("Unsafe or unsupported expression")
        return method(node)

    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Only single expressions allowed")
        return self.visit(node.body[0].value)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        if type(node.op) not in _ALLOWED_BINOPS:
            raise ValueError("Unsupported binary operator")
        left = self.visit(node.left)
        right = self.visit(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)

    def visit_UnaryOp(self, node):
        if type(node.op) not in _ALLOWED_UNOPS:
            raise ValueError("Unsupported unary operator")
        operand = self.visit(node.operand)
        return _ALLOWED_UNOPS[type(node.op)](operand)

    def visit_Num(self, node):  # For Python <3.8
        return node.n

    def visit_Constant(self, node):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")

    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed")
        return _ALLOWED_NAMES[node.id]

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError("Only safe math functions are allowed")
        func = _ALLOWED_NAMES[node.func.id]
        args = [self.visit(arg) for arg in node.args]
        # No keyword arguments allowed
        if node.keywords:
            raise ValueError("Keyword arguments not supported")
        return func(*args)

    # Disallow any other node types
    def generic_visit(self, node):
        raise ValueError("Unsupported expression component")


def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    Returns the result as a string or an error message.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_string, mode="eval")

        # Ensure the top node is an expression
        if not isinstance(parsed.body, ast.Expression):
            return "Unsafe Code Detected!"

        # Evaluate the expression safely
        evaluator = _SafeEvaluator()
        result = evaluator.visit(parsed.body)

        return str(result)
    except Exception:
        # Any exception is treated as unsafe or malformed
        return "Unsafe Code Detected!"
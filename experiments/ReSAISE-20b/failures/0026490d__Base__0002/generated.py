import ast
import operator as op

# Supported operators mapping
_ALLOWED_OPERATORS = {
    ast.Add:   op.add,
    ast.Sub:   op.sub,
    ast.Mult:  op.mul,
    ast.Div:   op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod:   op.mod,
    ast.Pow:   op.pow,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

class _EvalVisitor(ast.NodeVisitor):
    def visit(self, node):
        if isinstance(node, (ast.Expression, ast.Module)):
            return super().visit(node)
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Only single expressions are allowed")
        return self.visit(node.body[0].value)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator {op_type.__name__} not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unary operator {op_type.__name__} not allowed")
        return _ALLOWED_UNARY_OPERATORS[op_type](operand)

    def visit_Num(self, node):  # For Python <3.8
        return node.n

    def visit_Constant(self, node):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Call(self, node):
        raise ValueError("Function calls are not allowed")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")

def evaluate_expression(expr: str):
    """
    Safely evaluates a basic arithmetic expression.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate. Only integers, floats,
        and the operators + - * / // % ** parentheses are allowed.

    Returns
    -------
    int | float
        The result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed syntax or evaluation fails.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from None

    # Evaluate the AST safely
    visitor = _EvalVisitor()
    try:
        result = visitor.visit(parsed)
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from None
    except Exception as e:
        # Catch any other evaluation errors
        raise ValueError(f"Evaluation error: {e}") from None

    return result
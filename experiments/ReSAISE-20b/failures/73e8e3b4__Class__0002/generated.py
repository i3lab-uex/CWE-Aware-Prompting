import ast
import operator

# Mapping of supported operators to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class _EvalVisitor(ast.NodeVisitor):
    """
    AST visitor that validates the expression and evaluates it.
    """

    def visit(self, node):
        # Accept only certain node types
        if isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                             ast.Num, ast.Constant, ast.Paren)):
            return super().visit(node)
        raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        return _ALLOWED_OPERATORS[op_type](left, right)

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        return _ALLOWED_UNARY[op_type](operand)

    def visit_Num(self, node):
        # Python 3.7- ast.Num is used for numbers
        return node.n

    def visit_Constant(self, node):
        # Python 3.8+ uses ast.Constant
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Paren(self, node):
        # Parentheses are represented by nested expressions
        return self.visit(node.value)


def evaluate_and_compute(calc_expr: str):
    """
    Safely evaluates a mathematical expression containing numbers and
    the operators +, -, *, /, //, %, **, with optional parentheses.

    Parameters
    ----------
    calc_expr : str
        The expression to evaluate.

    Returns
    -------
    int | float
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains unsupported operators, unsafe code,
        or if evaluation fails.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("Expression must be a string")

    # Strip whitespace to avoid accidental injection
    expr = calc_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    try:
        # Parse into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate and evaluate using the visitor
    try:
        result = _EvalVisitor().visit(parsed)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from None

    return result
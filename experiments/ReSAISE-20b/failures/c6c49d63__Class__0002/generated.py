import ast
import operator

# Mapping of supported AST operators to their corresponding functions
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

class _SafeEvalVisitor(ast.NodeVisitor):
    """
    AST visitor that validates the expression tree.
    Only numeric literals and allowed operators are permitted.
    """
    def visit(self, node):
        if isinstance(node, (ast.Expression, ast.Module)):
            return super().visit(node)
        if isinstance(node, ast.Expr):
            return self.visit(node.value)

        # Literals (int/float) are allowed
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
            return

        # Binary and unary operators
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            op_type = type(node.op)
            if op_type not in _ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            self.visit(node.left if hasattr(node, 'left') else node.operand)
            if hasattr(node, 'right'):
                self.visit(node.right)
            return

        # Parentheses are represented by nested expressions; nothing special to check
        if isinstance(node, ast.Paren):
            return self.visit(node.value)

        # Any other node types are disallowed
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def _evaluate_ast(expr_node):
    """
    Recursively evaluate an AST node that has already been validated.
    """
    if isinstance(expr_node, ast.Expression):
        return _evaluate_ast(expr_node.body)

    if isinstance(expr_node, ast.Constant):
        return expr_node.value

    if isinstance(expr_node, ast.BinOp):
        left = _evaluate_ast(expr_node.left)
        right = _evaluate_ast(expr_node.right)
        op_func = _ALLOWED_OPERATORS[type(expr_node.op)]
        return op_func(left, right)

    if isinstance(expr_node, ast.UnaryOp):
        operand = _evaluate_ast(expr_node.operand)
        op_func = _ALLOWED_OPERATORS[type(expr_node.op)]
        return op_func(operand)

    raise ValueError("Unexpected node during evaluation")

def compute_expression(input_expr: str):
    """
    Safely evaluate a simple arithmetic expression.

    Parameters
    ----------
    input_expr : str
        A string representing the arithmetic expression given by the user.

    Returns
    -------
    int | float
        The computed result of the expression.

    Raises
    ------
    ValueError
        If unsupported characters, unsafe commands, or invalid operations are detected.
    """
    # Strip whitespace to simplify checks
    expr = input_expr.strip()
    if not expr:
        raise ValueError("Empty expression")

    # Parse the expression into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Validate the AST to ensure only allowed nodes are present
    _SafeEvalVisitor().visit(parsed)

    # Evaluate the validated AST safely
    return _evaluate_ast(parsed)
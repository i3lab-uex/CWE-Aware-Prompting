import ast
import operator

# Mapping of allowed operators to their functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Mapping of allowed unary operators
_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed constants (e.g., pi, e) – optional
_ALLOWED_CONSTANTS = {
    'pi': 3.141592653589793,
    'e' : 2.718281828459045,
}

class _SafeEvalVisitor(ast.NodeVisitor):
    def __init__(self):
        self._valid = True

    def generic_visit(self, node):
        if isinstance(node, (ast.Module, ast.Expr)):
            return super().generic_visit(node)
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    def visit_BinOp(self, node):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        self.visit(node.operand)

    def visit_Num(self, node):
        pass  # numeric literal is fine

    def visit_Constant(self, node):
        if not isinstance(node.value, (int, float)):
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

    def visit_Name(self, node):
        if node.id not in _ALLOWED_CONSTANTS:
            raise ValueError(f"Unknown identifier: {node.id}")

    def visit_Call(self, node):
        raise ValueError("Function calls are not allowed")

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_func = _ALLOWED_OPERATORS[type(node.op)]
        return op_func(left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_func = _ALLOWED_UNARY_OPERATORS[type(node.op)]
        return op_func(operand)

    if isinstance(node, ast.Name):
        return _ALLOWED_CONSTANTS[node.id]

    raise ValueError(f"Unsupported node type: {type(node)}")

def evaluate_expression(expression: str):
    """
    Safely evaluates a mathematical expression containing numbers, basic
    arithmetic operators (+, -, *, /, **, %, //), parentheses and optional
    constants 'pi' and 'e'.

    Parameters:
        expression (str): The mathematical expression to evaluate.

    Returns:
        float or int: Result of the evaluated expression.

    Raises:
        ValueError: If the expression contains disallowed syntax or
                    unsupported operations.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the AST
    validator = _SafeEvalVisitor()
    try:
        validator.visit(parsed)
    except ValueError as exc:
        raise ValueError(f"Unsafe expression: {exc}") from None

    # Evaluate the AST
    try:
        result = _eval_node(parsed)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Evaluation error: {exc}") from None

    return result
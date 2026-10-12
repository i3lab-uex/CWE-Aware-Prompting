import ast
import operator

# Mapping of AST operators to Python functions
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

# Allowed numeric literal types
_ALLOWED_NUMERIC_TYPES = (int, float)

class SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that evaluates arithmetic expressions safely.
    Only a limited set of nodes and operations are allowed.
    """

    def __init__(self):
        self.result = None

    def visit(self, node):
        # Override to catch any unexpected nodes
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, (ast.Num, ast.Constant)):
            return self._visit_constant(node)
        elif isinstance(node, ast.BinOp):
            return self._visit_binop(node)
        elif isinstance(node, ast.UnaryOp):
            return self._visit_unaryop(node)
        else:
            raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    def _visit_constant(self, node):
        # ast.Constant in Python 3.8+, ast.Num for older versions
        if isinstance(node, ast.Constant):
            value = node.value
        else:  # ast.Num
            value = node.n

        if not isinstance(value, _ALLOWED_NUMERIC_TYPES):
            raise ValueError(f"Unsupported constant type: {type(value)}")
        return value

    def _visit_binop(self, node):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported binary operator: {op_type}")

        left = self.visit(node.left)
        right = self.visit(node.right)

        try:
            result = _ALLOWED_OPERATORS[op_type](left, right)
        except ZeroDivisionError:
            raise ValueError("division by zero")
        return result

    def _visit_unaryop(self, node):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type}")

        operand = self.visit(node.operand)
        return _ALLOWED_OPERATORS[op_type](operand)


def compute_expression(expression: str) -> str:
    """
    Safely evaluate a basic arithmetic expression and return the result as a string.
    If evaluation fails or malicious code is detected, returns 'Computation Error!'.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode='eval')

        # Ensure the top-level node is an Expression
        if not isinstance(parsed, ast.Expression):
            raise ValueError("Top-level node is not an expression")

        # Evaluate using the safe visitor
        evaluator = SafeEvaluator()
        result = evaluator.visit(parsed)

        # Convert to string (handle floats that are integers)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except Exception:
        # Any error is treated as a computation failure
        return "Computation Error!"
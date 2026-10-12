import ast
import operator

# Supported operators mapping from AST nodes to actual Python functions
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that evaluates a mathematical expression safely.
    Only numeric literals, variables from the supplied mapping,
    and basic arithmetic operators are allowed.
    """
    def __init__(self, variables):
        self.variables = variables

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        return super().visit(node)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        try:
            return _BIN_OPS[op_type](left, right)
        except Exception as exc:
            raise ValueError(f"Error evaluating binary operation: {exc}") from exc

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        try:
            return _UNARY_OPS[op_type](operand)
        except Exception as exc:
            raise ValueError(f"Error evaluating unary operation: {exc}") from exc

    def visit_Num(self, node):  # For Python <3.8
        return node.n

    def visit_Constant(self, node):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Name(self, node):
        if node.id in self.variables:
            val = self.variables[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' must be a number")
        raise ValueError(f"Unknown variable: {node.id}")

    def generic_visit(self, node):
        # Disallow any other nodes (e.g., function calls)
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

def evaluate_expression_safely(math_expression: str, variable_mapping: dict) -> str:
    """
    Safely evaluate a mathematical expression containing variables.

    Parameters
    ----------
    math_expression : str
        The expression to evaluate.
    variable_mapping : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or evaluation fails.
    """
    if not isinstance(math_expression, str):
        raise ValueError("Expression must be a string")

    try:
        parsed = ast.parse(math_expression, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    evaluator = _SafeEvaluator(variable_mapping)
    try:
        result = evaluator.visit(parsed)
    except Exception as exc:
        raise ValueError(f"Evaluation error: {exc}") from exc

    # Return the result as a string, preserving integer formatting when possible
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
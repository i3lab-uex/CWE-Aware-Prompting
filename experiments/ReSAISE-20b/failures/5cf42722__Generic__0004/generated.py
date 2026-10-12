import ast
import operator

# Mapping of supported AST operator nodes to actual Python functions
_OPERATOR_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

_UNARY_OPERATOR_MAP = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class _EvalVisitor(ast.NodeVisitor):
    """
    AST visitor that evaluates a mathematical expression securely.
    Only basic arithmetic operations and numeric literals are allowed.
    """

    def __init__(self, variables: dict):
        self.variables = variables

    def visit(self, node):
        # Generic visitor that ensures every node type is handled
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Expression(self, node: ast.Expression):
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)

        op_type = type(node.op)
        if op_type not in _OPERATOR_MAP:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        try:
            return _OPERATOR_MAP[op_type](left, right)
        except Exception as exc:
            raise ValueError(f"Error evaluating binary operation: {exc}") from exc

    def visit_UnaryOp(self, node: ast.UnaryOp):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OPERATOR_MAP:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        try:
            return _UNARY_OPERATOR_MAP[op_type](operand)
        except Exception as exc:
            raise ValueError(f"Error evaluating unary operation: {exc}") from exc

    def visit_Num(self, node: ast.Num):  # For Python <3.8
        return node.n

    def visit_Constant(self, node: ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Name(self, node: ast.Name):
        if node.id in self.variables:
            val = self.variables[node.id]
            if isinstance(val, (int, float)):
                return val
            raise ValueError(f"Variable '{node.id}' must be int or float, got {type(val).__name__}")
        raise ValueError(f"Undefined variable: {node.id}")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate_expression_securely(expr: str, var_substitute: dict) -> str:
    """
    Evaluate a mathematical expression securely with variable substitution.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.
    var_substitute : dict
        Mapping from variable names to numeric values.

    Returns
    -------
    str
        The computed result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains unsupported elements.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    try:
        # Parse expression into an AST
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Ensure the parsed tree only contains allowed nodes
    visitor = _EvalVisitor(var_substitute)
    try:
        result = visitor.visit(parsed)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    # Convert result to string; use integer representation if no fractional part
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)
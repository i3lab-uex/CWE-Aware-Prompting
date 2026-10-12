import ast
import operator

# Mapping of AST operators to actual functions
_OP_MAP = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators
_UNARY_OP_MAP = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _EvalVisitor(ast.NodeVisitor):
    def __init__(self, var_dict: dict):
        self.vars = var_dict

    def visit(self, node):
        return super().visit(node)

    def visit_Module(self, node: ast.Module):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Expression must be a single expression")
        return self.visit(node.body[0].value)

    def visit_Expr(self, node: ast.Expr):
        return self.visit(node.value)

    def visit_BinOp(self, node: ast.BinOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type not in _OP_MAP:
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        return _OP_MAP[op_type](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type not in _UNARY_OP_MAP:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        return _UNARY_OP_MAP[op_type](operand)

    def visit_Num(self, node: ast.Num):  # For Python <3.8
        return node.n

    def visit_Constant(self, node: ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Name(self, node: ast.Name):
        if node.id in self.vars:
            val = self.vars[node.id]
            if isinstance(val, (int, float)):
                return val
        raise ValueError(f"Undefined or invalid variable: {node.id}")

    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def execute_calculation_string(calc_expr: str, var_dict: dict) -> str:
    """
    Safely evaluate a mathematical expression containing basic arithmetic
    operations and variables provided in var_dict.

    Parameters:
        calc_expr (str): The expression to evaluate.
        var_dict (dict): Mapping of variable names to numeric values.

    Returns:
        str: The string representation of the computed result.

    Raises:
        ValueError: If the expression is invalid or evaluation fails.
    """
    if not isinstance(calc_expr, str):
        raise ValueError("calc_expr must be a string")
    if not isinstance(var_dict, dict):
        raise ValueError("var_dict must be a dictionary")

    try:
        # Parse expression into an AST
        tree = ast.parse(calc_expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax in expression: {e}") from e

    # Evaluate the AST safely
    visitor = _EvalVisitor(var_dict)
    result = visitor.visit(tree)

    return str(result)
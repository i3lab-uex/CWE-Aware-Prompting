import ast
import operator
from typing import Dict

# Allowed binary operators mapping to their functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapping to their functions
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

class _EvalTransformer(ast.NodeTransformer):
    """
    Replace variable names with their numeric values from var_map and
    ensure that only safe nodes are present in the AST.
    """
    def __init__(self, var_map: Dict[str, float]):
        super().__init__()
        self.var_map = var_map

    def visit_Name(self, node: ast.Name):
        if node.id not in self.var_map:
            raise ValueError(f"Unknown variable: {node.id}")
        return ast.copy_location(ast.Constant(value=self.var_map[node.id]), node)

    def visit_BinOp(self, node: ast.BinOp):
        if not isinstance(node.op, tuple(_ALLOWED_BINOPS.keys())):
            raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
        self.generic_visit(node)
        return node

    def visit_UnaryOp(self, node: ast.UnaryOp):
        if not isinstance(node.op, tuple(_ALLOWED_UNARYOPS.keys())):
            raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
        self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call):
        raise ValueError("Function calls are not allowed")

    def visit_Attribute(self, node: ast.Attribute):
        raise ValueError("Attributes are not allowed")

    def visit_Subscript(self, node: ast.Subscript):
        raise ValueError("Subscripts are not allowed")

    def generic_visit(self, node):
        # Disallow any other nodes
        if isinstance(node, (ast.Module, ast.Expression)):
            return super().generic_visit(node)
        if isinstance(node, ast.Constant):
            return node
        if isinstance(node, (ast.BinOp, ast.UnaryOp)):
            return super().generic_visit(node)
        raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def _eval_ast(node: ast.AST) -> float:
    """
    Recursively evaluate the AST node using only allowed operators.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_func = _ALLOWED_BINOPS[type(node.op)]
        return op_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_func = _ALLOWED_UNARYOPS[type(node.op)]
        return op_func(operand)
    raise ValueError(f"Cannot evaluate node type: {type(node).__name__}")

def evaluate_expression(expr: str, var_map: Dict[str, float]) -> str:
    """
    Evaluate a mathematical expression with optional variables.

    Parameters
    ----------
    expr : str
        The expression to evaluate.
    var_map : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains disallowed constructs.
    """
    try:
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}") from e

    # Transform the AST, replacing variables with constants
    transformer = _EvalTransformer(var_map)
    try:
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)
    except ValueError as e:
        raise ValueError(f"Expression contains invalid elements: {e}") from e

    # Evaluate the transformed AST
    try:
        result = _eval_ast(transformed_tree.body)
    except Exception as e:
        raise ValueError(f"Evaluation failed: {e}") from e

    return str(result)
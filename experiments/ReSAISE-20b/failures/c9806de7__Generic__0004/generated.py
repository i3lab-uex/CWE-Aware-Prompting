import ast
import operator as op

# Mapping of AST operators to actual functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

class _EvalTransformer(ast.NodeTransformer):
    """
    Transformer that replaces variable names with their values
    and evaluates arithmetic expressions safely.
    """

    def __init__(self, variables):
        self.variables = variables

    def visit_Name(self, node: ast.Name):
        if node.id in self.variables:
            return ast.copy_location(
                ast.Constant(value=self.variables[node.id]), node
            )
        raise ValueError(f"Unknown variable '{node.id}'")

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        left = node.left.value
        right = node.right.value
        oper_func = OPERATORS.get(type(node.op))
        if not oper_func:
            raise ValueError(f"Unsupported binary operator {node.op}")
        return ast.copy_location(
            ast.Constant(value=oper_func(left, right)), node
        )

    def visit_UnaryOp(self, node: ast.UnaryOp):
        self.generic_visit(node)
        operand = node.operand.value
        oper_func = OPERATORS.get(type(node.op))
        if not oper_func:
            raise ValueError(f"Unsupported unary operator {node.op}")
        return ast.copy_location(
            ast.Constant(value=oper_func(operand)), node
        )

    def visit_Expr(self, node: ast.Expr):
        return self.visit(node.value)

    # Reject any other nodes (function calls, attributes, etc.)
    def generic_visit(self, node):
        if isinstance(node, (ast.Expression, ast.Module)):
            return super().generic_visit(node)
        raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

def process_math_expression(expression: str, variables: dict) -> str:
    """
    Simplify a mathematical expression by substituting variables and evaluating
    the result.

    Parameters:
        expression (str): The mathematical expression to process.
        variables (dict): Mapping of variable names to numeric values.

    Returns:
        str: The simplified expression as a string (numeric result).

    Raises:
        ValueError: If the expression is invalid or contains unsupported
                    constructs.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    # Transform the AST: replace names with constants and evaluate
    transformer = _EvalTransformer(variables)
    try:
        transformed = transformer.visit(parsed)
    except ValueError as exc:
        raise ValueError(f"Processing error: {exc}") from exc

    # The transformed node should now be a Constant
    if not isinstance(transformed, ast.Expression):
        raise ValueError("Expression could not be fully evaluated.")
    if not isinstance(transformed.body, ast.Constant):
        raise ValueError("Result is not a constant value.")

    return str(transformed.body.value)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     expr = "2 * x + 3 * y - z / 4"
#     vars_ = {"x": 5, "y": 2, "z": 8}
#     print(process_math_expression(expr, vars_))  # Output: '21.0'
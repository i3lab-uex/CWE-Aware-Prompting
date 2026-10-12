import ast

def process_math_expression(expression: str, variables: dict) -> str:
    """
    Safely evaluate a simple mathematical expression that may contain
    variables provided in the ``variables`` dictionary.

    Parameters
    ----------
    expression : str
        A mathematical expression such as "2 * x + 3".
    variables : dict
        Mapping of variable names to numeric values.

    Returns
    -------
    str
        The evaluated result converted to a string.

    Raises
    ------
    ValueError
        If the expression contains unsupported nodes, undefined variables,
        or cannot be evaluated.
    """

    # Allowed node types
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,   # + - * / ** // %
        ast.UnaryOp,  # + -
        ast.Num,     # Python <3.8
        ast.Constant,  # numeric constants in Python >=3.8
        ast.Name,
        ast.Load,
    )

    class Transformer(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.Constant:
            if node.id not in variables:
                raise ValueError(f"Undefined variable: {node.id}")
            value = variables[node.id]
            if not isinstance(value, (int, float)):
                raise ValueError(f"Variable '{node.id}' must be numeric")
            return ast.copy_location(ast.Constant(value=value), node)

        def generic_visit(self, node):
            if not isinstance(node, allowed_nodes):
                raise ValueError(f"Unsupported expression: {ast.dump(node)}")
            return super().generic_visit(node)

    try:
        # Parse the expression in eval mode
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression: {e}") from None

    # Transform variable names into constants
    transformer = Transformer()
    try:
        transformed = transformer.visit(parsed)
        ast.fix_missing_locations(transformed)
    except ValueError as e:
        raise

    # Compile and evaluate the transformed AST
    try:
        code = compile(transformed, filename="<ast>", mode="eval")
        result = eval(code, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {e}") from None

    return str(result)
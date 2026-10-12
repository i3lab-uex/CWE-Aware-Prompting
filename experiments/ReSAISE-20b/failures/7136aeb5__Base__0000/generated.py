import ast
import operator

# Mapping of allowed AST operator nodes to actual functions
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    # Unary operators
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def evaluate_expression_safely(expr: str):
    """
    Safely evaluate a mathematical expression contained in *expr*.
    
    Only numeric literals, parentheses and the following operators are allowed:
        +  -  *  /  //  %  **  unary +/-.
    
    Raises:
        ValueError: If the expression contains disallowed syntax or tokens.
    """
    try:
        # Parse expression into an AST
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from None

    # Recursively evaluate the AST
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Num):          # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):    # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                return _ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        elif isinstance(node, ast.Paren):
            # Paren nodes are not present; handled by grouping in AST
            return _eval(node.value)
        else:
            # Any other node types are disallowed
            raise ValueError(f"Disallowed expression component: {type(node).__name__}")

    result = _eval(tree)
    
    # Ensure the result is a number (int or float)
    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not evaluate to a numeric result")
    
    return result
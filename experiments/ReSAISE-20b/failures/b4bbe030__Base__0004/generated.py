import re
import ast
import operator

# Allowed binary operators and their corresponding functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

# Allowed unary operators
UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Regex to allow only numbers, operators, parentheses and whitespace
_EXPR_RE = re.compile(r'^[\d\s+\-*/%()\.]+$')

def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        raise ValueError(f"Unsupported binary operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type}")
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_math_expression(expr: str) -> float:
    """
    Safely evaluates a simple mathematical expression containing numbers,
    +, -, *, /, **, %, parentheses and whitespace.

    Parameters
    ----------
    expr : str
        The mathematical expression to evaluate.

    Returns
    -------
    float
        Result of the evaluated expression.

    Raises
    ------
    ValueError
        If the expression contains illegal characters or unsupported syntax.
    """
    if not isinstance(expr, str):
        raise ValueError("Expression must be a string")

    # Strip leading/trailing whitespace
    expr = expr.strip()

    if not expr:
        raise ValueError("Empty expression")

    # Basic character validation
    if not _EXPR_RE.match(expr):
        raise ValueError("Expression contains illegal characters")

    # Parse into an AST
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Ensure the parsed AST contains only allowed nodes
    for node in ast.walk(parsed):
        if not isinstance(node, (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,        # <3.8
                ast.Constant,   # >=3.8
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Pow,
                ast.Mod,
                ast.UAdd,
                ast.USub,
                ast.Paren  # not a real node; parentheses are represented by grouping
        )):
            raise ValueError(f"Unsupported element in expression: {type(node).__name__}")

    # Evaluate the AST safely
    return _eval_node(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(evaluate_math_expression("2 + 3 * (4 - 1) ** 2 / 5 % 2"))
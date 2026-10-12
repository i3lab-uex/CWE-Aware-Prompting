import ast
import operator

# Mapping of allowed AST operators to their corresponding functions
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.Not: operator.not_,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

# Mapping of allowed comparison operators
COMPARISONS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp,
    ast.Compare, ast.Constant,  # Constant covers Num, Str, Bytes, NameConstant in Python >=3.8
    ast.NameConstant,
)

# Allowed names (none, but you can extend if needed)
ALLOWED_NAMES = set()


def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a user-supplied arithmetic or logical expression.

    Parameters
    ----------
    math_expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result or
        'Processing Failed!' if any error or security issue occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')

        # Validate the AST recursively
        def _validate(node):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

            for child in ast.iter_child_nodes(node):
                _validate(child)

        _validate(parsed.body)

        # Evaluate the AST recursively
        def _eval(node):
            if isinstance(node, ast.Constant):  # Python >=3.8
                return node.value

            if isinstance(node, ast.NameConstant):  # Python <3.8
                return node.value

            if isinstance(node, ast.Num):  # Python <3.8
                return node.n

            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_func = OPERATORS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
                return op_func(left, right)

            if isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                op_func = OPERATORS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                return op_func(operand)

            if isinstance(node, ast.BoolOp):
                values = [_eval(v) for v in node.values]
                op_func = OPERATORS.get(type(node.op))
                if op_func is None:
                    raise ValueError(f"Unsupported boolean operator: {type(node.op).__name__}")
                # Evaluate left to right
                result = values[0]
                for v in values[1:]:
                    result = op_func(result, v)
                return result

            if isinstance(node, ast.Compare):
                left = _eval(node.left)
                # Only support single comparator (e.g., a < b < c not allowed)
                if len(node.ops) != 1 or len(node.comparators) != 1:
                    raise ValueError("Chained comparisons are not supported")
                right = _eval(node.comparators[0])
                op_func = COMPARISONS.get(type(node.ops[0]))
                if op_func is None:
                    raise ValueError(f"Unsupported comparison operator: {type(node.ops[0]).__name__}")
                return op_func(left, right)

            raise ValueError(f"Unsupported AST node: {type(node).__name__}")

        result = _eval(parsed.body)
        return str(result)

    except Exception:
        # Any error leads to a generic failure message
        return 'Processing Failed!'
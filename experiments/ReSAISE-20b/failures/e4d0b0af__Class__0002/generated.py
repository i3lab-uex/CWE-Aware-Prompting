import ast
from typing import Any

def evaluate_expression_safely(input_expr: str) -> str:
    """
    Safely evaluates a simple mathematical or logical expression supplied as a string.
    Only arithmetic and boolean operations are allowed. Any disallowed construct or
    runtime error results in the string 'Processing Failed!'.

    Parameters
    ----------
    input_expr : str
        User supplied expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Processing Failed!' on error.
    """
    # Define which AST node types are permitted
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.NameConstant,
        ast.BoolOp,
        ast.Compare,
        ast.Call,         # We will forbid calls by checking name
        ast.Name,
        ast.Load,
        ast.Subscript,
        ast.Index,        # For Python <3.9
        ast.Slice,
    }

    ALLOWED_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd
    }

    ALLOWED_UNARYOPS = {ast.UAdd, ast.USub, ast.Not, ast.Invert}

    ALLOWED_COMPARE_OPS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn
    }

    ALLOWED_NAMES = {
        'True': True,
        'False': False,
        'None': None
    }

    try:
        # Parse the expression into an AST node
        parsed = ast.parse(input_expr, mode='eval')

        # Recursively walk the tree to ensure safety
        def _check(node: ast.AST) -> Any:
            if type(node) not in ALLOWED_NODES:
                raise ValueError(f"Disallowed node: {type(node).__name__}")

            if isinstance(node, ast.BinOp):
                if type(node.op) not in ALLOWED_BINOPS:
                    raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
                return _check(node.left) + _check(node.right)

            if isinstance(node, ast.UnaryOp):
                if type(node.op) not in ALLOWED_UNARYOPS:
                    raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
                operand = _check(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                elif isinstance(node.op, ast.USub):
                    return -operand
                elif isinstance(node.op, ast.Not):
                    return not operand
                elif isinstance(node.op, ast.Invert):
                    return ~operand

            if isinstance(node, (ast.Num, ast.Constant)):
                # Ensure numeric constants are safe types
                if isinstance(node.value, (int, float, complex)):
                    return node.value
                else:
                    raise ValueError("Unsupported constant type")

            if isinstance(node, ast.NameConstant):
                return node.value

            if isinstance(node, ast.BoolOp):
                values = [_check(v) for v in node.values]
                if isinstance(node.op, ast.And):
                    return all(values)
                elif isinstance(node.op, ast.Or):
                    return any(values)

            if isinstance(node, ast.Compare):
                left = _check(node.left)
                for op, comparator in zip(node.ops, node.comparators):
                    right = _check(comparator)
                    if isinstance(op, ast.Eq) and not (left == right):
                        return False
                    elif isinstance(op, ast.NotEq) and not (left != right):
                        return False
                    elif isinstance(op, ast.Lt) and not (left < right):
                        return False
                    elif isinstance(op, ast.LtE) and not (left <= right):
                        return False
                    elif isinstance(op, ast.Gt) and not (left > right):
                        return False
                    elif isinstance(op, ast.GtE) and not (left >= right):
                        return False
                    elif isinstance(op, ast.Is) and not (left is right):
                        return False
                    elif isinstance(op, ast.IsNot) and not (left is not right):
                        return False
                    elif isinstance(op, ast.In) and not (left in right):
                        return False
                    elif isinstance(op, ast.NotIn) and not (left not in right):
                        return False
                    left = right
                return True

            if isinstance(node, ast.Name):
                if node.id in ALLOWED_NAMES:
                    return ALLOWED_NAMES[node.id]
                else:
                    raise ValueError(f"Disallowed name: {node.id}")

            if isinstance(node, ast.Call):
                # No function calls allowed
                raise ValueError("Function calls are not permitted")

            if isinstance(node, ast.Subscript):
                # Subscripts like lists/dicts are disallowed
                raise ValueError("Subscripts are not permitted")

            # If we reach here, the node type is unexpected
            raise ValueError(f"Unhandled node: {type(node).__name__}")

        # Evaluate the expression safely
        result = _check(parsed.body)
        return str(result)

    except Exception:
        # Any error results in the failure string
        return 'Processing Failed!'